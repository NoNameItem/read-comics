import pytest
from django.conf import settings
from pymongo import MongoClient

from read_comics.characters.models import Character
from read_comics.issues.models import Issue
from read_comics.missing_issues.tasks import BaseMissingIssuesTask

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
