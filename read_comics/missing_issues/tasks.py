from datetime import date, datetime, timedelta

from billiard.exceptions import WorkerLostError
from celery import Task, signature
from django.conf import settings
from django.db import IntegrityError, OperationalError, connection
from django.db.models import Count, Q
from pymongo import MongoClient
from pymongo.errors import CursorNotFound

from config import celery_app
from read_comics.characters.models import Character
from read_comics.concepts.models import Concept
from read_comics.issues.models import Issue
from read_comics.locations.models import Location
from read_comics.objects.models import Object
from read_comics.people.models import Person
from read_comics.publishers.models import Publisher
from read_comics.story_arcs.models import StoryArc
from read_comics.teams.models import Team
from read_comics.volumes.models import Volume

from .models import IgnoredIssue, IgnoredPublisher, IgnoredVolume, MissingIssue


class BaseMissingIssuesTask(Task):
    autoretry_for = (OperationalError, WorkerLostError, CursorNotFound)
    retry_kwargs = {"max_retries": 10}
    retry_backoff = True
    retry_backoff_max = 60

    MONGO_COLLECTION = "comicvine_issues"
    VOLUMES_COLLECTION = "comicvine_volumes"
    PUBLISHERS_COLLECTION = "comicvine_publishers"

    BATCH_SIZE = 500

    VOLUME_PROJECTION = {
        "_id": 0,
        "id": 1,
        "site_detail_url": 1,
        "name": 1,
        "start_year": 1,
        "publisher.id": 1,
        "publisher.name": 1,
    }

    LOOKUP = {"from": "comicvine_volumes", "localField": "volume.id", "foreignField": "id", "as": "volume"}

    PROJECT = {
        "_id": 0,
        "comicvine_id": "$id",
        "comicvine_url": "$site_detail_url",
        "name": 1,
        "number": "$issue_number",
        "cover_date": 1,
        "volume_comicvine_id": {"$arrayElemAt": ["$volume.id", 0]},
        "volume_comicvine_url": {"$arrayElemAt": ["$volume.site_detail_url", 0]},
        "volume_name": {"$arrayElemAt": ["$volume.name", 0]},
        "volume_start_year": {"$arrayElemAt": ["$volume.start_year", 0]},
        "publisher_name": {"$arrayElemAt": ["$volume.publisher.name", 0]},
        "publisher_comicvine_id": {"$arrayElemAt": ["$volume.publisher.id", 0]},
        "publisher_comicvine_url": {"$arrayElemAt": ["$publisher.site_detail_url", 0]},
    }

    FILTER_PATH = None
    MODEL = None

    @staticmethod
    def get_existing_issues(obj):
        return list(obj.issues.values_list("comicvine_id", flat=True))

    @staticmethod
    def get_ignored_issues():
        return list(IgnoredIssue.objects.values_list("comicvine_id", flat=True))

    @staticmethod
    def get_ignored_volumes():
        return list(IgnoredVolume.objects.values_list("comicvine_id", flat=True))

    @staticmethod
    def get_ignored_publishers():
        return list(IgnoredPublisher.objects.values_list("comicvine_id", flat=True))

    def get_object_filter(self, db, obj, volumes):
        return {self.FILTER_PATH: obj.comicvine_id}

    def get_candidates(self, db, obj, object_filter):
        existing = set(self.get_existing_issues(obj))
        cursor = db[self.MONGO_COLLECTION].find(object_filter, {"_id": 0, "id": 1, "volume.id": 1})
        candidates = {}
        for doc in cursor:
            if doc["id"] in existing:
                continue
            candidates[doc["id"]] = {"id": doc["id"], "volume_id": (doc.get("volume") or {}).get("id")}
        return [candidates[issue_id] for issue_id in sorted(candidates)]

    def load_volumes(self, db, volume_ids, volumes):
        missing = {volume_id for volume_id in volume_ids if volume_id is not None and volume_id not in volumes}
        if not missing:
            return
        for doc in db[self.VOLUMES_COLLECTION].find({"id": {"$in": list(missing)}}, self.VOLUME_PROJECTION):
            volumes.setdefault(doc["id"], doc)

    @staticmethod
    def check_batch(issue_ids, volume_ids, publisher_ids):
        query = " union all ".join(
            f"select '{kind}', comicvine_id from {model._meta.db_table} where comicvine_id = any(%s)"
            for kind, model in (
                ("issue", Issue),
                ("ignored_issue", IgnoredIssue),
                ("ignored_volume", IgnoredVolume),
                ("ignored_publisher", IgnoredPublisher),
            )
        )
        found = {"issue": set(), "ignored_issue": set(), "ignored_volume": set(), "ignored_publisher": set()}
        with connection.cursor() as cursor:
            cursor.execute(query, [list(issue_ids), list(issue_ids), list(volume_ids), list(publisher_ids)])
            for kind, comicvine_id in cursor.fetchall():
                found[kind].add(comicvine_id)
        return found

    def check_candidates(self, batch, volumes):
        issue_ids = [candidate["id"] for candidate in batch]
        volume_ids = {candidate["volume_id"] for candidate in batch if candidate["volume_id"] is not None}
        publisher_ids = {
            publisher["id"]
            for volume_id in volume_ids
            for publisher in [(volumes.get(volume_id) or {}).get("publisher") or {}]
            if publisher.get("id") is not None
        }
        found = self.check_batch(issue_ids, volume_ids, publisher_ids)

        to_write = []
        in_library_ids = set()
        ignored_ids = set()
        for candidate in batch:
            issue_id = candidate["id"]
            volume_id = candidate["volume_id"]
            publisher = (volumes.get(volume_id) or {}).get("publisher") or {}
            if (
                issue_id in found["ignored_issue"]
                or volume_id in found["ignored_volume"]
                or publisher.get("id") in found["ignored_publisher"]
            ):
                ignored_ids.add(issue_id)
            elif issue_id in found["issue"]:
                in_library_ids.add(issue_id)
            else:
                to_write.append(candidate)
        return to_write, in_library_ids, ignored_ids

    def get_match(self, obj):
        return {
            "$and": [
                {self.FILTER_PATH: obj.comicvine_id},
                {"id": {"$not": {"$in": self.get_existing_issues(obj)}}},
                {"id": {"$not": {"$in": self.get_ignored_issues()}}},
                {"volume.id": {"$not": {"$in": self.get_ignored_volumes()}}},
            ]
        }

    def get_issues_from_mongo(self, obj):
        client = MongoClient(settings.MONGO_URL)
        db = client.get_default_database()
        collection = db[self.MONGO_COLLECTION]

        issues = collection.aggregate(
            [
                {"$match": self.get_match(obj)},
                {"$lookup": self.LOOKUP},
                {"$match": {"volume.publisher.id": {"$not": {"$in": self.get_ignored_publishers()}}}},
                {
                    "$lookup": {
                        "from": "comicvine_publishers",
                        "localField": "volume.publisher.id",
                        "foreignField": "id",
                        "as": "publisher",
                    }
                },
                {"$project": self.PROJECT},
            ]
        )
        client.close()
        return issues  # noqa R504

    @staticmethod
    def get_or_create_missing_issue(mongo_missing_issue):
        comicvine_id = mongo_missing_issue.pop("comicvine_id")
        try:
            missing_issue, _ = MissingIssue.objects.get_or_create(
                comicvine_id=comicvine_id, defaults=mongo_missing_issue
            )
        except IntegrityError:
            missing_issue = MissingIssue.objects.get(comicvine_id=comicvine_id)
        cover_date = mongo_missing_issue.get("cover_date", None)
        if cover_date:
            missing_issue.cover_date = datetime.fromisoformat(cover_date)
        missing_issue.name = mongo_missing_issue.get("name", None)
        missing_issue.comicvine_url = mongo_missing_issue.get("comicvine_url", None)
        missing_issue.number = mongo_missing_issue.get("number", None)
        missing_issue.volume_comicvine_id = mongo_missing_issue.get("volume_comicvine_id", None)
        missing_issue.volume_comicvine_url = mongo_missing_issue.get("volume_comicvine_url", None)
        missing_issue.volume_name = mongo_missing_issue.get("volume_name", None)
        missing_issue.volume_start_year = mongo_missing_issue.get("volume_start_year", None)
        missing_issue.publisher_name = mongo_missing_issue.get("publisher_name", None)
        missing_issue.publisher_comicvine_id = mongo_missing_issue.get("publisher_comicvine_id", None)
        missing_issue.publisher_comicvine_url = mongo_missing_issue.get("publisher_comicvine_url", None)
        if Issue.objects.filter(comicvine_id=comicvine_id).exists():
            MissingIssue.objects.filter(comicvine_id=comicvine_id).delete()
            return None
        else:
            if missing_issue.skip and missing_issue.skip_date < date.today() - timedelta(days=settings.SKIP_DAYS):
                missing_issue.skip = False
                missing_issue.skip_date = None
            missing_issue.set_numerical_number()
            missing_issue.save()
            return missing_issue

    @staticmethod
    def add_missing_issue(obj, missing_issue):
        obj.missing_issues.add(missing_issue)

    def process_mongo_issues(self, obj, mongo_missing_issues):
        for mongo_missing_issue in mongo_missing_issues:
            # Check ignored on insert. Issue/volume/publisher can be marked as ignored between mongo query
            # start and missing issue processing
            if (
                mongo_missing_issue.get("comicvine_id") not in self.get_ignored_issues()
                and mongo_missing_issue.get("volume_comicvine_id") not in self.get_ignored_volumes()
                and mongo_missing_issue.get("publisher_comicvine_id") not in self.get_ignored_publishers()
            ):
                missing_issue = self.get_or_create_missing_issue(mongo_missing_issue)
                if missing_issue:
                    self.add_missing_issue(obj, missing_issue)

    def get_objects(self):
        return self.MODEL.objects.annotate(
            issue_count=Count("issues", distinct=True), watchers_count=Count("watchers", distinct=True)
        ).filter(Q(issue_count__gt=0) | Q(watchers_count__gt=0))

    @staticmethod
    def check_object(obj):
        return obj.issues.exists() or obj.watchers.exists()

    def run(self, *args, **kwargs):
        try:
            pk = kwargs["pk"]
            obj = self.MODEL.objects.get(pk=pk)
            if self.check_object(obj):
                mongo_missing_issues = self.get_issues_from_mongo(obj)
                self.process_mongo_issues(obj, mongo_missing_issues)
        except KeyError:
            for obj in self.get_objects():
                task = signature(self.name, kwargs={"pk": obj.pk})
                task.delay()


class VolumeMissingIssuesTask(BaseMissingIssuesTask):
    FILTER_PATH = "volume.id"
    MODEL = Volume


volume_missing_issues_task = celery_app.register_task(VolumeMissingIssuesTask())


class PublisherMissingIssuesTask(BaseMissingIssuesTask):
    FILTER_PATH = "volume.publisher.id"
    MODEL = Publisher

    def get_objects(self):
        ignored_publishers = list(IgnoredPublisher.objects.values_list("comicvine_id", flat=True))

        return self.MODEL.objects.exclude(comicvine_id__in=ignored_publishers)

    @staticmethod
    def check_object(obj):
        # True if publisher not ignored
        return not IgnoredPublisher.objects.filter(comicvine_id=obj.comicvine_id).exists()

    def get_match(self, obj):
        client = MongoClient(settings.MONGO_URL)
        db = client.get_default_database()
        collection = db["comicvine_volumes"]

        volumes = collection.find({"publisher.id": obj.comicvine_id}, {"id": 1})
        volume_ids = [volume["id"] for volume in volumes]
        client.close()

        return {
            "$and": [
                {"volume.id": {"$in": volume_ids}},
                {"id": {"$not": {"$in": self.get_existing_issues(obj)}}},
                {"id": {"$not": {"$in": self.get_ignored_issues()}}},
                {"volume.id": {"$not": {"$in": self.get_ignored_volumes()}}},
            ]
        }

    def get_issues_from_mongo(self, obj):
        client = MongoClient(settings.MONGO_URL)
        db = client.get_default_database()
        collection = db[self.MONGO_COLLECTION]

        issues = collection.aggregate(
            [
                {"$match": self.get_match(obj)},
                {"$lookup": self.LOOKUP},
                {
                    "$lookup": {
                        "from": "comicvine_publishers",
                        "localField": "volume.publisher.id",
                        "foreignField": "id",
                        "as": "publisher",
                    }
                },
                {"$project": self.PROJECT},
            ]
        )
        client.close()
        return issues  # noqa R504

    @staticmethod
    def get_existing_issues(obj):
        return list(Issue.objects.filter(volume__publisher=obj).values_list("comicvine_id", flat=True))


publisher_missing_issues_task = celery_app.register_task(PublisherMissingIssuesTask())


class CharacterMissingIssuesTask(BaseMissingIssuesTask):
    FILTER_PATH = "character_credits.id"
    MODEL = Character


character_missing_issues_task = celery_app.register_task(CharacterMissingIssuesTask())


class ConceptMissingIssuesTask(BaseMissingIssuesTask):
    FILTER_PATH = "concept_credits.id"
    MODEL = Concept


concept_missing_issues_task = celery_app.register_task(ConceptMissingIssuesTask())


class LocationMissingIssuesTask(BaseMissingIssuesTask):
    FILTER_PATH = "location_credits.id"
    MODEL = Location


location_missing_issues_task = celery_app.register_task(LocationMissingIssuesTask())


class ObjectMissingIssuesTask(BaseMissingIssuesTask):
    FILTER_PATH = "object_credits.id"
    MODEL = Object


object_missing_issues_task = celery_app.register_task(ObjectMissingIssuesTask())


class PersonMissingIssuesTask(BaseMissingIssuesTask):
    FILTER_PATH = "person_credits.id"
    MODEL = Person


person_missing_issues_task = celery_app.register_task(PersonMissingIssuesTask())


class StoryArcMissingIssuesTask(BaseMissingIssuesTask):
    FILTER_PATH = "story_arc_credits.id"
    MODEL = StoryArc


story_arc_missing_issues_task = celery_app.register_task(StoryArcMissingIssuesTask())


class TeamMissingIssuesTask(BaseMissingIssuesTask):
    FILTER_PATH = "team_credits.id"
    MODEL = Team


team_missing_issues_task = celery_app.register_task(TeamMissingIssuesTask())
