import os
import re
import sys

from celery import Celery
from celery.schedules import crontab

current_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(current_path, "read_comics"))
print(sys.path)

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

app = Celery("read_comics")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.task_queue_max_priority = 10
app.conf.task_default_priority = 5

TASK_REGEX = re.compile(r"^(read_comics\.)?(?P<app>[^.]+)\.tasks\.(?P<task>.*)$")
CRAWL_TASK_REGEX = re.compile(r"(^[^_]+|story_arcs)_(increment_|skip_existing_)*update$")
MISSING_ISSUES_QUEUES = {
    "CharacterMissingIssuesTask": "read_comics_characters",
    "ConceptMissingIssuesTask": "read_comics_concepts",
    "LocationMissingIssuesTask": "read_comics_locations",
    "ObjectMissingIssuesTask": "read_comics_objects",
    "PersonMissingIssuesTask": "read_comics_people",
    "PublisherMissingIssuesTask": "read_comics_publishers",
    "StoryArcMissingIssuesTask": "read_comics_story_arcs",
    "TeamMissingIssuesTask": "read_comics_teams",
    "VolumeMissingIssuesTask": "read_comics_volumes",
}


def route_tasks(name, args, kwargs, options, task=None, **kw):
    match = TASK_REGEX.match(name)
    if match:
        if CRAWL_TASK_REGEX.match(match.group("task")):
            return {"queue": "read_comics_spiders"}

        if match.group("app") == "missing_issues":
            return {"queue": MISSING_ISSUES_QUEUES[match.group("task")]}

        if match.group("app") in (
            "characters",
            "concepts",
            "issues",
            "locations",
            "objects",
            "people",
            "powers",
            "publishers",
            "story_arcs",
            "teams",
            "volumes",
        ):
            return {"queue": f'read_comics_{match.group("app")}'}
    return None


app.conf.task_default_queue = "read_comics_default"
app.conf.task_create_missing_queues = True
app.conf.task_routes = (route_tasks,)

app.conf.beat_schedule = {
    # Get new comics from Digital Ocean Space every day at 04:00 AM
    # "get-from-space": {
    #     "task": "read_comics.publishers.tasks.PublishersSpaceTask",
    #     "schedule": crontab(minute=0, hour="4"),
    #     "args": (),
    #     "kwargs": {"prefix": "comics/"},
    #     "options": {"priority": 0},
    # },
    # Purge comics deleted from Digital Ocean Space every day at 04:00 AM
    "purge-deleted": {
        "task": "read_comics.issues.tasks.purge_deleted",
        "schedule": crontab(minute=0, hour="4"),
    },
    # Refresh data from Comicvine API every day at 03:00 AM UTC
    "refresh-characters": {
        "task": "read_comics.characters.tasks.CharactersRefreshTask",
        "schedule": crontab(minute=0, hour="3"),
    },
    "refresh-concepts": {
        "task": "read_comics.concepts.tasks.ConceptsRefreshTask",
        "schedule": crontab(minute=0, hour="3"),
    },
    "refresh-issues": {
        "task": "read_comics.issues.tasks.IssuesRefreshTask",
        "schedule": crontab(minute=0, hour="3"),
    },
    "refresh-locations": {
        "task": "read_comics.locations.tasks.LocationsRefreshTask",
        "schedule": crontab(minute=0, hour="3"),
    },
    "refresh-objects": {
        "task": "read_comics.objects.tasks.ObjectsRefreshTask",
        "schedule": crontab(minute=0, hour="3"),
    },
    "refresh-people": {
        "task": "read_comics.people.tasks.PeopleRefreshTask",
        "schedule": crontab(minute=0, hour="3"),
    },
    "refresh-powers": {
        "task": "read_comics.powers.tasks.PowersRefreshTask",
        "schedule": crontab(minute=0, hour="3"),
    },
    "refresh-publishers": {
        "task": "read_comics.publishers.tasks.PublishersRefreshTask",
        "schedule": crontab(minute=0, hour="3"),
    },
    "refresh-story-arcs": {
        "task": "read_comics.story_arcs.tasks.StoryArcsRefreshTask",
        "schedule": crontab(minute=0, hour="3"),
    },
    "refresh-teams": {
        "task": "read_comics.teams.tasks.TeamsRefreshTask",
        "schedule": crontab(minute=0, hour="3"),
    },
    "refresh-volumes": {
        "task": "read_comics.volumes.tasks.VolumesRefreshTask",
        "schedule": crontab(minute=0, hour="3"),
    },
    "refresh-publishers-missing-issues": {
        "task": "read_comics.missing_issues.tasks.PublisherMissingIssuesTask",
        "schedule": crontab(minute=0, hour="7", day_of_week="fri"),
    },
    "refresh-volumes-missing-issues": {
        "task": "read_comics.missing_issues.tasks.VolumeMissingIssuesTask",
        "schedule": crontab(minute=0, hour="7", day_of_week="fri"),
    },
    "refresh-character-missing-issues": {
        "task": "read_comics.missing_issues.tasks.CharacterMissingIssuesTask",
        "schedule": crontab(minute=0, hour="7", day_of_week="fri"),
    },
    "refresh-story-arcs-missing-issues": {
        "task": "read_comics.missing_issues.tasks.StoryArcMissingIssuesTask",
        "schedule": crontab(minute=0, hour="7", day_of_week="fri"),
    },
    "refresh-teams-missing-issues": {
        "task": "read_comics.missing_issues.tasks.TeamMissingIssuesTask",
        "schedule": crontab(minute=0, hour="7", day_of_week="fri"),
    },
    "refresh-person-missing-issues": {
        "task": "read_comics.missing_issues.tasks.PersonMissingIssuesTask",
        "schedule": crontab(minute=0, hour="7", day_of_week="fri"),
    },
    "full_increment_update": {
        "task": "read_comics.utils.tasks.full_increment_update",
        "schedule": crontab(minute=0, hour="0"),
    },
    # "characters_increment_update": {
    #     "task": "read_comics.characters.tasks.characters_increment_update",
    #     "schedule": crontab(minute=0, hour="0"),
    # },
    # "concepts_increment_update": {
    #     "task": "read_comics.concepts.tasks.concepts_increment_update",
    #     "schedule": crontab(minute=0, hour="0"),
    # },
    # "issues_increment_update": {
    #     "task": "read_comics.issues.tasks.issues_increment_update",
    #     "schedule": crontab(minute=0, hour="0"),
    # },
    # "locations_increment_update": {
    #     "task": "read_comics.locations.tasks.locations_increment_update",
    #     "schedule": crontab(minute=0, hour="0"),
    # },
    # "objects_increment_update": {
    #     "task": "read_comics.objects.tasks.objects_increment_update",
    #     "schedule": crontab(minute=0, hour="0"),
    # },
    # "people_increment_update": {
    #     "task": "read_comics.people.tasks.people_increment_update",
    #     "schedule": crontab(minute=0, hour="0"),
    # },
    # "powers_increment_update": {
    #     "task": "read_comics.powers.tasks.powers_increment_update",
    #     "schedule": crontab(minute=0, hour="0"),
    # },
    # "publishers_increment_update": {
    #     "task": "read_comics.publishers.tasks.publishers_increment_update",
    #     "schedule": crontab(minute=0, hour="0"),
    # },
    # "story_arcs_increment_update": {
    #     "task": "read_comics.story_arcs.tasks.story_arcs_increment_update",
    #     "schedule": crontab(minute=0, hour="0"),
    # },
    # "teams_increment_update": {
    #     "task": "read_comics.teams.tasks.teams_increment_update",
    #     "schedule": crontab(minute=0, hour="0"),
    # },
    # "volumes_increment_update": {
    #     "task": "read_comics.volumes.tasks.volumes_increment_update",
    #     "schedule": crontab(minute=0, hour="0"),
    # }
}

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
