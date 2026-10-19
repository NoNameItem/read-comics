import pytest

from read_comics.missing_issues.tasks import character_missing_issues_task

pytestmark = pytest.mark.django_db

CREDIT = {"character_credits": [{"id": 1699}]}


def test_check_object_uses_issues_or_watchers(character, make_issue):
    assert character_missing_issues_task.check_object(character) is False
    make_issue(1).characters.add(character)
    assert character_missing_issues_task.check_object(character) is True


def test_candidates_exclude_existing_and_are_sorted(mongo_db, issues_col, character, make_issue):
    issues_col.insert_many(
        [
            {"id": 30, "volume": {"id": 300}, **CREDIT},
            {"id": 10, "volume": {"id": 100}, **CREDIT},
            {"id": 20, "volume": {"id": 200}, **CREDIT},
            {"id": 40, "volume": {"id": 400}, "character_credits": [{"id": 1}]},
        ]
    )
    make_issue(20).characters.add(character)
    task = character_missing_issues_task
    object_filter = task.get_object_filter(mongo_db, character, {})
    assert task.get_candidates(mongo_db, character, object_filter) == [
        {"id": 10, "volume_id": 100},
        {"id": 30, "volume_id": 300},
    ]


def test_candidates_keep_issue_without_volume(mongo_db, issues_col, character):
    issues_col.insert_many([{"id": 1, **CREDIT}, {"id": 2, "volume": None, **CREDIT}])
    object_filter = character_missing_issues_task.get_object_filter(mongo_db, character, {})
    assert character_missing_issues_task.get_candidates(mongo_db, character, object_filter) == [
        {"id": 1, "volume_id": None},
        {"id": 2, "volume_id": None},
    ]
