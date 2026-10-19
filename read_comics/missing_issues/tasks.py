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

    DATA_FIELDS = (
        "comicvine_url",
        "name",
        "number",
        "numerical_number",
        "cover_date",
        "volume_comicvine_id",
        "volume_comicvine_url",
        "volume_name",
        "volume_start_year",
        "publisher_name",
        "publisher_comicvine_id",
        "publisher_comicvine_url",
    )

    FILTER_PATH = None
    MODEL = None
    LINK_FK = None

    @staticmethod
    def get_existing_issues(obj):
        return list(obj.issues.values_list("comicvine_id", flat=True))

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
    def get_volume_publisher(volumes, volume_id):
        return (volumes.get(volume_id) or {}).get("publisher") or {}

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
        publishers = (self.get_volume_publisher(volumes, volume_id) for volume_id in volume_ids)
        publisher_ids = {publisher["id"] for publisher in publishers if publisher.get("id") is not None}
        found = self.check_batch(issue_ids, volume_ids, publisher_ids)

        to_write = []
        in_library_ids = set()
        ignored_ids = set()
        for candidate in batch:
            issue_id = candidate["id"]
            volume_id = candidate["volume_id"]
            publisher = self.get_volume_publisher(volumes, volume_id)
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

    def get_rows(self, db, object_filter, candidates, volumes):
        issue_ids = [candidate["id"] for candidate in candidates]
        issue_projection = {"_id": 0, "id": 1, "site_detail_url": 1, "name": 1, "issue_number": 1, "cover_date": 1}
        issues = {}
        cursor = db[self.MONGO_COLLECTION].find({"$and": [object_filter, {"id": {"$in": issue_ids}}]}, issue_projection)
        for doc in cursor:
            issues[doc["id"]] = doc

        publisher_ids = {
            publisher["id"]
            for publisher in (self.get_volume_publisher(volumes, candidate["volume_id"]) for candidate in candidates)
            if publisher.get("id") is not None
        }
        publisher_urls = {}
        if publisher_ids:
            publishers = db[self.PUBLISHERS_COLLECTION].find(
                {"id": {"$in": list(publisher_ids)}}, {"_id": 0, "id": 1, "site_detail_url": 1}
            )
            for doc in publishers:
                publisher_urls[doc["id"]] = doc.get("site_detail_url")

        volume_ids = {candidate["id"]: candidate["volume_id"] for candidate in candidates}
        rows = []
        for issue_id in sorted(issues):
            issue = issues[issue_id]
            volume_id = volume_ids[issue_id]
            volume = volumes.get(volume_id) or {}
            publisher = self.get_volume_publisher(volumes, volume_id)
            rows.append(
                {
                    "comicvine_id": issue_id,
                    "comicvine_url": issue.get("site_detail_url"),
                    "name": issue.get("name"),
                    "number": issue.get("issue_number"),
                    "cover_date": issue.get("cover_date"),
                    "volume_comicvine_id": volume.get("id"),
                    "volume_comicvine_url": volume.get("site_detail_url"),
                    "volume_name": volume.get("name"),
                    "volume_start_year": volume.get("start_year"),
                    "publisher_name": publisher.get("name"),
                    "publisher_comicvine_id": publisher.get("id"),
                    "publisher_comicvine_url": publisher_urls.get(publisher.get("id")),
                }
            )
        return rows

    def build_write_plan(self, rows):
        existing = {
            missing_issue.comicvine_id: missing_issue
            for missing_issue in MissingIssue.objects.filter(comicvine_id__in=[row["comicvine_id"] for row in rows])
        }
        skip_border = date.today() - timedelta(days=settings.SKIP_DAYS)
        plan = {"create": [], "update": [], "skip_reset_ids": []}
        for row in rows:
            missing_issue = existing.get(row["comicvine_id"])
            if missing_issue is None:
                missing_issue = MissingIssue(comicvine_id=row["comicvine_id"])
                plan["create"].append(missing_issue)
                old_values = None
            else:
                old_values = {name: getattr(missing_issue, name) for name in self.DATA_FIELDS}
                if missing_issue.skip and missing_issue.skip_date and missing_issue.skip_date < skip_border:
                    plan["skip_reset_ids"].append(missing_issue.comicvine_id)
            for name in self.DATA_FIELDS:
                if name == "numerical_number":
                    continue
                value = row.get(name)
                if name == "cover_date":
                    if not value:
                        continue
                    value = datetime.fromisoformat(value).date()
                setattr(missing_issue, name, MissingIssue._meta.get_field(name).to_python(value))
            missing_issue.set_numerical_number()
            if old_values is not None and any(getattr(missing_issue, name) != old_values[name] for name in old_values):
                plan["update"].append(missing_issue)
        return plan

    def plan_batch(self, db, object_filter, batch, volumes):
        self.load_volumes(db, [candidate["volume_id"] for candidate in batch], volumes)
        to_write, in_library_ids, _ = self.check_candidates(batch, volumes)
        rows = self.get_rows(db, object_filter, to_write, volumes)
        return {**self.build_write_plan(rows), "rows": rows, "candidates": to_write, "delete_ids": in_library_ids}

    def apply_batch(self, obj, plan, volumes):
        if plan["delete_ids"]:
            MissingIssue.objects.filter(comicvine_id__in=plan["delete_ids"]).delete()
        MissingIssue.objects.bulk_create(plan["create"], ignore_conflicts=True)
        MissingIssue.objects.bulk_update(plan["update"], self.DATA_FIELDS)
        if plan["skip_reset_ids"]:
            MissingIssue.objects.filter(
                comicvine_id__in=plan["skip_reset_ids"],
                skip=True,
                skip_date__lt=date.today() - timedelta(days=settings.SKIP_DAYS),
            ).update(skip=False, skip_date=None)
        if not plan["rows"]:
            return
        comicvine_ids = [row["comicvine_id"] for row in plan["rows"]]
        missing_issues = list(MissingIssue.objects.filter(comicvine_id__in=comicvine_ids).order_by("comicvine_id"))
        self.add_missing_issues(obj, missing_issues)
        # Issues ignored or added to the library while the batch was written must not keep their rows
        _, in_library_ids, ignored_ids = self.check_candidates(plan["candidates"], volumes)
        if in_library_ids or ignored_ids:
            MissingIssue.objects.filter(comicvine_id__in=in_library_ids | ignored_ids).delete()

    def add_missing_issues(self, obj, missing_issues):
        if self.LINK_FK:
            missing_issues = [
                missing_issue
                for missing_issue in missing_issues
                if getattr(missing_issue, f"{self.LINK_FK}_id") != obj.pk
            ]
        try:
            obj.missing_issues.add(*missing_issues)
        except IntegrityError:
            # A row was deleted after it was re-read: link only the rows that still exist.
            # Relies on autocommit and DEFERRABLE INITIALLY DEFERRED FKs: the error surfaces when .add()'s own atomic
            # block commits; an outer transaction.atomic here or in apply_batch would raise it outside this except.
            pks = [missing_issue.pk for missing_issue in missing_issues]
            obj.missing_issues.add(*MissingIssue.objects.filter(pk__in=pks).order_by("comicvine_id"))

    def process_object(self, obj):
        client = MongoClient(settings.MONGO_URL)
        try:
            db = client.get_default_database()
            volumes = {}
            object_filter = self.get_object_filter(db, obj, volumes)
            candidates = self.get_candidates(db, obj, object_filter)
            for start in range(0, len(candidates), self.BATCH_SIZE):
                batch = candidates[start : start + self.BATCH_SIZE]
                self.apply_batch(obj, self.plan_batch(db, object_filter, batch, volumes), volumes)
        finally:
            client.close()

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
                self.process_object(obj)
        except KeyError:
            for obj in self.get_objects():
                task = signature(self.name, kwargs={"pk": obj.pk})
                task.delay()


class VolumeMissingIssuesTask(BaseMissingIssuesTask):
    FILTER_PATH = "volume.id"
    MODEL = Volume
    LINK_FK = "volume"


volume_missing_issues_task = celery_app.register_task(VolumeMissingIssuesTask())


class PublisherMissingIssuesTask(BaseMissingIssuesTask):
    MODEL = Publisher
    LINK_FK = "publisher"

    def get_objects(self):
        ignored_publishers = list(IgnoredPublisher.objects.values_list("comicvine_id", flat=True))

        return self.MODEL.objects.exclude(comicvine_id__in=ignored_publishers)

    @staticmethod
    def check_object(obj):
        # True if publisher not ignored
        return not IgnoredPublisher.objects.filter(comicvine_id=obj.comicvine_id).exists()

    def get_object_filter(self, db, obj, volumes):
        for doc in db[self.VOLUMES_COLLECTION].find({"publisher.id": obj.comicvine_id}, self.VOLUME_PROJECTION):
            volumes[doc["id"]] = doc
        ignored = self.check_batch([], volumes, [])["ignored_volume"]
        return {"volume.id": {"$in": sorted(set(volumes) - ignored)}}

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
