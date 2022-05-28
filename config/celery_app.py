import os
import sys

from celery import Celery
from celery.schedules import crontab

current_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(current_path, "read_comics"))
print(sys.path)

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("read_comics")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.broker_transport_options = {
    "priority_steps": list(range(10)),
    "queue_order_strategy": "priority",
}
app.conf.task_default_priority = 5

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
        "schedule": crontab(minute=0, hour="7"),
    },
    "characters_increment_update": {
        "task": "read_comics.characters.tasks.characters_increment_update",
        "schedule": crontab(minute=0, hour="0"),
    },
    "concepts_increment_update": {
        "task": "read_comics.concepts.tasks.concepts_increment_update",
        "schedule": crontab(minute=0, hour="0"),
    },
    "issues_increment_update": {
        "task": "read_comics.issues.tasks.issues_increment_update",
        "schedule": crontab(minute=0, hour="0"),
    },
    "locations_increment_update": {
        "task": "read_comics.locations.tasks.locations_increment_update",
        "schedule": crontab(minute=0, hour="0"),
    },
    "objects_increment_update": {
        "task": "read_comics.objects.tasks.objects_increment_update",
        "schedule": crontab(minute=0, hour="0"),
    },
    "people_increment_update": {
        "task": "read_comics.people.tasks.people_increment_update",
        "schedule": crontab(minute=0, hour="0"),
    },
    "powers_increment_update": {
        "task": "read_comics.powers.tasks.powers_increment_update",
        "schedule": crontab(minute=0, hour="0"),
    },
    "publishers_increment_update": {
        "task": "read_comics.publishers.tasks.publishers_increment_update",
        "schedule": crontab(minute=0, hour="0"),
    },
    "story_arcs_increment_update": {
        "task": "read_comics.story_arcs.tasks.story_arcs_increment_update",
        "schedule": crontab(minute=0, hour="0"),
    },
    "teams_increment_update": {
        "task": "read_comics.teams.tasks.teams_increment_update",
        "schedule": crontab(minute=0, hour="0"),
    },
    "volumes_increment_update": {
        "task": "read_comics.volumes.tasks.volumes_increment_update",
        "schedule": crontab(minute=0, hour="0"),
    }
}
app.conf.timezone = "UTC"

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
