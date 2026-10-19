import pytest

from read_comics.missing_issues.models import IgnoredIssue, IgnoredPublisher, IgnoredVolume
from read_comics.missing_issues.tasks import BaseMissingIssuesTask, character_missing_issues_task

pytestmark = pytest.mark.django_db


def test_load_volumes_fetches_only_missing(mongo_db, volumes_col):
    volumes_col.insert_many(
        [
            {"id": 100, "name": "from mongo"},
            {"id": 101, "name": "B", "publisher": {"id": 5, "name": "P"}, "description": "dropped"},
        ]
    )
    volumes = {100: {"id": 100, "name": "cached"}}
    character_missing_issues_task.load_volumes(mongo_db, [100, 101, None], volumes)
    assert volumes == {
        100: {"id": 100, "name": "cached"},
        101: {"id": 101, "name": "B", "publisher": {"id": 5, "name": "P"}},
    }


def test_check_batch_finds_each_kind(make_issue):
    make_issue(1)
    IgnoredIssue.objects.create(comicvine_id=2, volume_name="v")
    IgnoredVolume.objects.create(comicvine_id=100, name="v")
    IgnoredPublisher.objects.create(comicvine_id=500)
    assert BaseMissingIssuesTask.check_batch([1, 2, 3], [100, 101], [500, 501]) == {
        "issue": {1},
        "ignored_issue": {2},
        "ignored_volume": {100},
        "ignored_publisher": {500},
    }
    assert BaseMissingIssuesTask.check_batch([], [], []) == {
        "issue": set(),
        "ignored_issue": set(),
        "ignored_volume": set(),
        "ignored_publisher": set(),
    }


def test_check_candidates_priority_and_sources(make_issue):  # Review Focus 2
    make_issue(1)
    make_issue(5)
    IgnoredIssue.objects.create(comicvine_id=1, volume_name="v")
    IgnoredVolume.objects.create(comicvine_id=100, name="v")
    IgnoredPublisher.objects.create(comicvine_id=500)
    batch = [
        {"id": 1, "volume_id": 101},  # ignored issue that is also in library -> ignored wins
        {"id": 2, "volume_id": 100},  # ignored by embedded volume id, volume doc missing
        {"id": 3, "volume_id": 102},  # publisher of its volume is ignored
        {"id": 4, "volume_id": None},  # no volume -> kept
        {"id": 5, "volume_id": 103},  # in library -> delete
        {"id": 6, "volume_id": 104},  # volume without publisher -> kept
        {"id": 7, "volume_id": 105},  # volume doc missing, not ignored -> kept
    ]
    volumes = {
        101: {"id": 101},
        102: {"id": 102, "publisher": {"id": 500}},
        103: {"id": 103},
        104: {"id": 104, "publisher": None},
    }
    to_write, in_library, ignored = character_missing_issues_task.check_candidates(batch, volumes)
    assert [c["id"] for c in to_write] == [4, 6, 7]
    assert in_library == {5}
    assert ignored == {1, 2, 3}
