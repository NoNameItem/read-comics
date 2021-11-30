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
    stats = dict()
    stats['characters_count'] = Character.objects.queued().count()
    stats['concepts_count'] = Concept.objects.queued().count()
    stats['issues_count'] = Issue.objects.queued().count()
    stats['locations_count'] = Location.objects.queued().count()
    stats['objects_count'] = Object.objects.queued().count()
    stats['people_count'] = Person.objects.queued().count()
    stats['powers_count'] = Power.objects.queued().count()
    stats['publishers_count'] = Publisher.objects.queued().count()
    stats['story_arcs_count'] = StoryArc.objects.queued().count()
    stats['teams_count'] = Team.objects.queued().count()
    stats['volumes_count'] = Volume.objects.queued().count()

    stats['total'] = sum(stats.values())

    return stats


def get_matched_stats():
    stats = dict()
    stats['characters_count'] = Character.objects.matched().count()
    stats['concepts_count'] = Concept.objects.matched().count()
    stats['issues_count'] = Issue.objects.matched().count()
    stats['locations_count'] = Location.objects.matched().count()
    stats['objects_count'] = Object.objects.matched().count()
    stats['people_count'] = Person.objects.matched().count()
    stats['powers_count'] = Power.objects.matched().count()
    stats['publishers_count'] = Publisher.objects.matched().count()
    stats['story_arcs_count'] = StoryArc.objects.matched().count()
    stats['teams_count'] = Team.objects.matched().count()
    stats['volumes_count'] = Volume.objects.matched().count()

    stats['total'] = sum(stats.values())

    return stats


def get_not_matched_stats():
    stats = dict()
    stats['characters_count'] = Character.objects.not_matched().count()
    stats['concepts_count'] = Concept.objects.not_matched().count()
    stats['issues_count'] = Issue.objects.not_matched().count()
    stats['locations_count'] = Location.objects.not_matched().count()
    stats['objects_count'] = Object.objects.not_matched().count()
    stats['people_count'] = Person.objects.not_matched().count()
    stats['powers_count'] = Power.objects.not_matched().count()
    stats['publishers_count'] = Publisher.objects.not_matched().count()
    stats['story_arcs_count'] = StoryArc.objects.not_matched().count()
    stats['teams_count'] = Team.objects.not_matched().count()
    stats['volumes_count'] = Volume.objects.not_matched().count()

    stats['total'] = sum(stats.values())

    return stats


def get_was_matched_stats():
    stats = dict()
    stats['characters_count'] = Character.objects.was_matched().count()
    stats['concepts_count'] = Concept.objects.was_matched().count()
    stats['issues_count'] = Issue.objects.was_matched().count()
    stats['locations_count'] = Location.objects.was_matched().count()
    stats['objects_count'] = Object.objects.was_matched().count()
    stats['people_count'] = Person.objects.was_matched().count()
    stats['powers_count'] = Power.objects.was_matched().count()
    stats['publishers_count'] = Publisher.objects.was_matched().count()
    stats['story_arcs_count'] = StoryArc.objects.was_matched().count()
    stats['teams_count'] = Team.objects.was_matched().count()
    stats['volumes_count'] = Volume.objects.was_matched().count()

    stats['total'] = sum(stats.values())

    return stats


# noinspection DuplicatedCode
def get_not_comicvine_actual_count(model):
    objects_list = list(
        model.objects.exclude(
            comicvine_status=model.ComicvineStatus.QUEUED
        ).values(
            'id',
            'comicvine_id',
            'comicvine_last_match'
        )
    )
    comicvine_ids = [x['comicvine_id'] for x in objects_list]
    objects_map = {
        x['comicvine_id']: {
            'id': x['id'],
            'comicvine_last_match': x['comicvine_last_match']
        }
        for x in objects_list
    }

    # Get data from Mongo
    client = MongoClient(settings.MONGO_URL)
    db = client.get_default_database()
    collection = db[model.MONGO_COLLECTION]
    comicvine_objects = list(collection.find({'id': {'$in': comicvine_ids}}, {'id': 1, 'crawl_date': 1}))

    # Counting
    count = 0
    for comicvine_object in comicvine_objects:
        obj = objects_map.get(comicvine_object['id'])
        if obj:
            if obj['comicvine_last_match'] is None \
               or obj['comicvine_last_match'] <= pytz.UTC.localize(comicvine_object['crawl_date']):
                count += 1

    return count


def get_not_actual_stats():
    stats = dict()
    stats['characters_count'] = get_not_comicvine_actual_count(Character)
    stats['concepts_count'] = get_not_comicvine_actual_count(Concept)
    stats['issues_count'] = get_not_comicvine_actual_count(Issue)
    stats['locations_count'] = get_not_comicvine_actual_count(Location)
    stats['objects_count'] = get_not_comicvine_actual_count(Object)
    stats['people_count'] = get_not_comicvine_actual_count(Person)
    stats['powers_count'] = get_not_comicvine_actual_count(Power)
    stats['publishers_count'] = get_not_comicvine_actual_count(Publisher)
    stats['story_arcs_count'] = get_not_comicvine_actual_count(StoryArc)
    stats['teams_count'] = get_not_comicvine_actual_count(Team)
    stats['volumes_count'] = get_not_comicvine_actual_count(Volume)

    stats['total'] = sum(stats.values())

    return stats
