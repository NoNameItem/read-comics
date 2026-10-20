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
    task = character_missing_issues_task
    batch = task.get_candidates(mongo_db, character, task.get_object_filter(mongo_db, character))
    return task.plan_batch(mongo_db, batch)


@pytest.mark.usefixtures("run_caches")
@pytest.mark.parametrize("change", ["ignore_volume", "add_to_library"])
def test_apply_batch_drops_row_changed_after_planning(mongo_db, seeded, linked_character, make_issue, change):
    plan = planned(mongo_db, linked_character)
    if change == "ignore_volume":
        IgnoredVolume.objects.create(comicvine_id=100, name="Vol")
    else:
        make_issue(10)
    character_missing_issues_task.apply_batch(linked_character, plan)
    assert not MissingIssue.objects.filter(comicvine_id=10).exists()


@pytest.mark.usefixtures("run_caches")
def test_apply_batch_keeps_skip_set_during_run(mongo_db, seeded, linked_character):
    MissingIssue.objects.create(comicvine_id=10, name="Old")
    plan = planned(mongo_db, linked_character)
    MissingIssue.objects.filter(comicvine_id=10).update(skip=True, skip_date=date.today())
    character_missing_issues_task.apply_batch(linked_character, plan)
    mi = MissingIssue.objects.get(comicvine_id=10)
    assert (mi.name, mi.skip) == ("N", True)


@pytest.mark.usefixtures("run_caches")
def test_apply_batch_keeps_skip_renewed_during_run(mongo_db, seeded, linked_character, settings):
    settings.SKIP_DAYS = 7
    MissingIssue.objects.create(comicvine_id=10, skip=True, skip_date=date.today() - timedelta(days=8))
    plan = planned(mongo_db, linked_character)
    assert plan["skip_reset_ids"] == [10]
    MissingIssue.objects.filter(comicvine_id=10).update(skip_date=date.today())
    character_missing_issues_task.apply_batch(linked_character, plan)
    assert MissingIssue.objects.get(comicvine_id=10).skip is True


def test_run_uses_fresh_caches_and_drops_them(mongo_db, seeded, linked_character, monkeypatch):
    task = character_missing_issues_task
    monkeypatch.setattr(task, "volumes", {100: {"id": 100, "name": "stale"}})
    monkeypatch.setattr(task, "publisher_urls", {500: "stale"})
    task.run(pk=linked_character.pk)
    mi = MissingIssue.objects.get(comicvine_id=10)
    assert (mi.volume_name, mi.publisher_comicvine_url) == ("Vol", "https://cv/p500")
    assert task.volumes is None and task.publisher_urls is None


def test_run_drops_caches_when_processing_fails(mongo_db, seeded, linked_character, monkeypatch):
    def fail(*args, **kwargs):
        raise RuntimeError("write failed")

    monkeypatch.setattr(BaseMissingIssuesTask, "apply_batch", fail)
    task = character_missing_issues_task
    with pytest.raises(RuntimeError):
        task.run(pk=linked_character.pk)
    assert task.volumes is None and task.publisher_urls is None


def test_run_processes_several_batches(mongo_db, seeded, linked_character, issues_col, volumes_col, monkeypatch):
    monkeypatch.setattr(BaseMissingIssuesTask, "BATCH_SIZE", 1)
    for issue_id, volume_id in ((11, 100), (12, 101)):
        issues_col.insert_one({"id": issue_id, "volume": {"id": volume_id}, "character_credits": [{"id": 1699}]})
    volumes_col.insert_one({"id": 101, "name": "Vol2"})
    character_missing_issues_task.run(pk=linked_character.pk)
    names = dict(MissingIssue.objects.values_list("comicvine_id", "volume_name"))
    assert names == {10: "Vol", 11: "Vol", 12: "Vol2"}
    assert set(linked_character.missing_issues.values_list("comicvine_id", flat=True)) == {10, 11, 12}


@pytest.mark.usefixtures("run_caches")
def test_apply_batch_links_row_created_concurrently(mongo_db, seeded, linked_character):  # Review Focus 4
    plan = planned(mongo_db, linked_character)
    MissingIssue.objects.create(comicvine_id=10, name="other task")
    character_missing_issues_task.apply_batch(linked_character, plan)
    assert MissingIssue.objects.filter(comicvine_id=10).count() == 1
    assert linked_character.missing_issues.filter(comicvine_id=10).exists()


@pytest.mark.django_db(transaction=True)  # deferred FK checks fire only on a real commit
def test_add_missing_issues_skips_deleted_rows(character):
    mi1, mi2 = MissingIssue.objects.create(comicvine_id=1), MissingIssue.objects.create(comicvine_id=2)
    MissingIssue.objects.filter(pk=mi2.pk).delete()
    character_missing_issues_task.add_missing_issues(character, [mi1, mi2])
    assert list(character.missing_issues.all()) == [mi1]
