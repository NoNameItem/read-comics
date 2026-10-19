from datetime import date, timedelta

import pytest

from read_comics.missing_issues.models import IgnoredVolume, MissingIssue
from read_comics.missing_issues.tasks import (
    BaseMissingIssuesTask,
    character_missing_issues_task,
    volume_missing_issues_task,
)
from read_comics.volumes.models import Volume

pytestmark = pytest.mark.django_db


def test_run_creates_rows_and_links(mongo_db, seeded, linked_character):
    character_missing_issues_task.run(pk=linked_character.pk)
    mi = MissingIssue.objects.get(comicvine_id=10)
    assert list(linked_character.missing_issues.all()) == [mi]
    assert (mi.volume_name, mi.publisher_comicvine_url, mi.cover_date) == ("Vol", "https://cv/p500", date(2020, 1, 31))


def test_run_volume_sets_fk(mongo_db, seeded, make_issue):
    volume = Volume.objects.create(comicvine_id=100, name="Vol")
    make_issue(99, volume=volume)
    volume_missing_issues_task.run(pk=volume.pk)
    assert MissingIssue.objects.get(comicvine_id=10).volume == volume


def test_run_deletes_row_for_issue_in_library(mongo_db, seeded, linked_character, make_issue):
    make_issue(10)  # in library but not linked to the character
    MissingIssue.objects.create(comicvine_id=10)
    character_missing_issues_task.run(pk=linked_character.pk)
    assert not MissingIssue.objects.filter(comicvine_id=10).exists()


def test_run_leaves_ignored_row_untouched(mongo_db, seeded, linked_character):
    IgnoredVolume.objects.create(comicvine_id=100, name="Vol")
    MissingIssue.objects.create(comicvine_id=10, name="kept")
    character_missing_issues_task.run(pk=linked_character.pk)
    assert MissingIssue.objects.get(comicvine_id=10).name == "kept"
    assert not linked_character.missing_issues.exists()


def test_run_resets_expired_skip(mongo_db, seeded, linked_character, settings):
    settings.SKIP_DAYS = 7
    MissingIssue.objects.create(comicvine_id=10, skip=True, skip_date=date.today() - timedelta(days=8))
    character_missing_issues_task.run(pk=linked_character.pk)
    assert MissingIssue.objects.filter(comicvine_id=10, skip=False, skip_date=None).exists()


def test_run_without_candidates_plans_nothing(mongo_db, seeded, linked_character, make_issue, monkeypatch):  # RF 3
    make_issue(10).characters.add(linked_character)
    monkeypatch.setattr(BaseMissingIssuesTask, "plan_batch", lambda *a, **k: pytest.fail("planned"))
    character_missing_issues_task.run(pk=linked_character.pk)
    assert not MissingIssue.objects.exists()


def planned(mongo_db, character):
    task, volumes = character_missing_issues_task, {}
    object_filter = task.get_object_filter(mongo_db, character, volumes)
    batch = task.get_candidates(mongo_db, character, object_filter)
    return task.plan_batch(mongo_db, object_filter, batch, volumes), volumes


@pytest.mark.parametrize("change", ["ignore_volume", "add_to_library"])
def test_apply_batch_drops_row_changed_after_planning(mongo_db, seeded, linked_character, make_issue, change):
    plan, volumes = planned(mongo_db, linked_character)
    if change == "ignore_volume":
        IgnoredVolume.objects.create(comicvine_id=100, name="Vol")
    else:
        make_issue(10)
    character_missing_issues_task.apply_batch(linked_character, plan, volumes)
    assert not MissingIssue.objects.filter(comicvine_id=10).exists()


def test_apply_batch_keeps_skip_set_during_run(mongo_db, seeded, linked_character):
    MissingIssue.objects.create(comicvine_id=10, name="Old")
    plan, volumes = planned(mongo_db, linked_character)
    MissingIssue.objects.filter(comicvine_id=10).update(skip=True, skip_date=date.today())
    character_missing_issues_task.apply_batch(linked_character, plan, volumes)
    mi = MissingIssue.objects.get(comicvine_id=10)
    assert (mi.name, mi.skip) == ("N", True)


def test_apply_batch_links_row_created_concurrently(mongo_db, seeded, linked_character):  # Review Focus 4
    plan, volumes = planned(mongo_db, linked_character)
    MissingIssue.objects.create(comicvine_id=10, name="other task")
    character_missing_issues_task.apply_batch(linked_character, plan, volumes)
    assert MissingIssue.objects.filter(comicvine_id=10).count() == 1
    assert linked_character.missing_issues.filter(comicvine_id=10).exists()


@pytest.mark.django_db(transaction=True)  # deferred FK checks fire only on a real commit
def test_add_missing_issues_skips_deleted_rows(character):
    mi1, mi2 = MissingIssue.objects.create(comicvine_id=1), MissingIssue.objects.create(comicvine_id=2)
    MissingIssue.objects.filter(pk=mi2.pk).delete()
    character_missing_issues_task.add_missing_issues(character, [mi1, mi2])
    assert list(character.missing_issues.all()) == [mi1]
