import pytest
from django.conf import settings
from pymongo import MongoClient

from read_comics.characters.models import Character
from read_comics.issues.models import Issue
from read_comics.missing_issues.tasks import (
    BaseMissingIssuesTask,
    character_missing_issues_task,
    publisher_missing_issues_task,
)

ISSUES = "test_missing_issues_issues"
VOLUMES = "test_missing_issues_volumes"
PUBLISHERS = "test_missing_issues_publishers"


@pytest.fixture
def mongo_db(monkeypatch):
    monkeypatch.setattr(BaseMissingIssuesTask, "MONGO_COLLECTION", ISSUES)
    monkeypatch.setattr(BaseMissingIssuesTask, "VOLUMES_COLLECTION", VOLUMES)
    monkeypatch.setattr(BaseMissingIssuesTask, "PUBLISHERS_COLLECTION", PUBLISHERS)
    client = MongoClient(settings.MONGO_URL)
    db = client.get_default_database()
    for name in (ISSUES, VOLUMES, PUBLISHERS):
        db.drop_collection(name)
    yield db
    for name in (ISSUES, VOLUMES, PUBLISHERS):
        db.drop_collection(name)
    client.close()


@pytest.fixture
def run_caches(monkeypatch):
    # Methods called outside process_object need the per-run caches it would set up
    for task in (character_missing_issues_task, publisher_missing_issues_task):
        monkeypatch.setattr(task, "volumes", {})
        monkeypatch.setattr(task, "publisher_urls", {})


@pytest.fixture
def issues_col(mongo_db):
    return mongo_db[ISSUES]


@pytest.fixture
def volumes_col(mongo_db):
    return mongo_db[VOLUMES]


@pytest.fixture
def publishers_col(mongo_db):
    return mongo_db[PUBLISHERS]


@pytest.fixture
def character(db):
    return Character.objects.create(comicvine_id=1699, name="Batman")


@pytest.fixture
def make_issue(db):
    def _make_issue(comicvine_id, **fields):
        return Issue.objects.create(comicvine_id=comicvine_id, space_key=f"test/{comicvine_id}.cbz", **fields)

    return _make_issue


@pytest.fixture
def seeded(issues_col, volumes_col, publishers_col):
    issues_col.insert_one(
        {
            "id": 10,
            "volume": {"id": 100},
            "character_credits": [{"id": 1699}],
            "site_detail_url": "https://cv/i10",
            "name": "N",
            "issue_number": "1",
            "cover_date": "2020-01-31",
            "description": "dropped",
        }
    )
    volumes_col.insert_one(
        {
            "id": 100,
            "site_detail_url": "https://cv/v100",
            "name": "Vol",
            "start_year": "1940",
            "publisher": {"id": 500, "name": "Pub"},
        }
    )
    publishers_col.insert_one({"id": 500, "site_detail_url": "https://cv/p500"})


@pytest.fixture
def linked_character(character, make_issue):
    make_issue(99).characters.add(character)
    return character
