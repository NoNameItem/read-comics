import pytz
from django.conf import settings
from pymongo import MongoClient

from read_comics.characters.models import Character
from read_comics.concepts.models import Concept
from read_comics.issues.models import Issue
from read_comics.locations.models import Location
from read_comics.objects.models import Object
from read_comics.people.models import Person
from read_comics.powers.models import Power
from read_comics.publishers.models import Publisher
from read_comics.story_arcs.models import StoryArc
from read_comics.teams.models import Team
from read_comics.volumes.models import Volume


def get_queued_stats():
    stats = {
        "characters_count": Character.objects.queued().count(),
        "concepts_count": Concept.objects.queued().count(),
        "issues_count": Issue.objects.queued().count(),
        "locations_count": Location.objects.queued().count(),
        "objects_count": Object.objects.queued().count(),
        "people_count": Person.objects.queued().count(),
        "powers_count": Power.objects.queued().count(),
        "publishers_count": Publisher.objects.queued().count(),
        "story_arcs_count": StoryArc.objects.queued().count(),
        "teams_count": Team.objects.queued().count(),
        "volumes_count": Volume.objects.queued().count(),
    }
    stats["total"] = sum(stats.values())

    return stats


def get_matched_stats():
    stats = {
        "characters_count": Character.objects.matched().count(),
        "concepts_count": Concept.objects.matched().count(),
        "issues_count": Issue.objects.matched().count(),
        "locations_count": Location.objects.matched().count(),
        "objects_count": Object.objects.matched().count(),
        "people_count": Person.objects.matched().count(),
        "powers_count": Power.objects.matched().count(),
        "publishers_count": Publisher.objects.matched().count(),
        "story_arcs_count": StoryArc.objects.matched().count(),
        "teams_count": Team.objects.matched().count(),
        "volumes_count": Volume.objects.matched().count(),
    }
    stats["total"] = sum(stats.values())

    return stats


def get_not_matched_stats():
    stats = {
        "characters_count": Character.objects.not_matched().count(),
        "concepts_count": Concept.objects.not_matched().count(),
        "issues_count": Issue.objects.not_matched().count(),
        "locations_count": Location.objects.not_matched().count(),
        "objects_count": Object.objects.not_matched().count(),
        "people_count": Person.objects.not_matched().count(),
        "powers_count": Power.objects.not_matched().count(),
        "publishers_count": Publisher.objects.not_matched().count(),
        "story_arcs_count": StoryArc.objects.not_matched().count(),
        "teams_count": Team.objects.not_matched().count(),
        "volumes_count": Volume.objects.not_matched().count(),
    }
    stats["total"] = sum(stats.values())

    return stats


def get_was_matched_stats():
    stats = {
        "characters_count": Character.objects.was_matched().count(),
        "concepts_count": Concept.objects.was_matched().count(),
        "issues_count": Issue.objects.was_matched().count(),
        "locations_count": Location.objects.was_matched().count(),
        "objects_count": Object.objects.was_matched().count(),
        "people_count": Person.objects.was_matched().count(),
        "powers_count": Power.objects.was_matched().count(),
        "publishers_count": Publisher.objects.was_matched().count(),
        "story_arcs_count": StoryArc.objects.was_matched().count(),
        "teams_count": Team.objects.was_matched().count(),
        "volumes_count": Volume.objects.was_matched().count(),
    }
    stats["total"] = sum(stats.values())

    return stats


# noinspection DuplicatedCode
def get_not_comicvine_actual_count(model):
    objects_list = list(
        model.objects.exclude(comicvine_status=model.ComicvineStatus.QUEUED).values(
            "id", "comicvine_id", "comicvine_last_match"
        )
    )
    comicvine_ids = [x["comicvine_id"] for x in objects_list]
    objects_map = {
        x["comicvine_id"]: {"id": x["id"], "comicvine_last_match": x["comicvine_last_match"]} for x in objects_list
    }

    # Get data from Mongo
    client = MongoClient(settings.MONGO_URL)
    db = client.get_default_database()
    collection = db[model.MONGO_COLLECTION]
    comicvine_objects = list(collection.find({"id": {"$in": comicvine_ids}}, {"id": 1, "crawl_date": 1}))
    client.close()

    # Counting
    count = 0
    for comicvine_object in comicvine_objects:
        obj = objects_map.get(comicvine_object["id"])
        if obj and (
            obj["comicvine_last_match"] is None
            or obj["comicvine_last_match"] <= pytz.UTC.localize(comicvine_object["crawl_date"])
        ):
            count += 1

    return count


def get_not_actual_stats():
    stats = {
        "characters_count": get_not_comicvine_actual_count(Character),
        "concepts_count": get_not_comicvine_actual_count(Concept),
        "issues_count": get_not_comicvine_actual_count(Issue),
        "locations_count": get_not_comicvine_actual_count(Location),
        "objects_count": get_not_comicvine_actual_count(Object),
        "people_count": get_not_comicvine_actual_count(Person),
        "powers_count": get_not_comicvine_actual_count(Power),
        "publishers_count": get_not_comicvine_actual_count(Publisher),
        "story_arcs_count": get_not_comicvine_actual_count(StoryArc),
        "teams_count": get_not_comicvine_actual_count(Team),
        "volumes_count": get_not_comicvine_actual_count(Volume),
    }
    stats["total"] = sum(stats.values())

    return stats
