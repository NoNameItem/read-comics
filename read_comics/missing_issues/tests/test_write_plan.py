from datetime import date, timedelta

import pytest

from read_comics.missing_issues.models import MissingIssue
from read_comics.missing_issues.tasks import character_missing_issues_task

pytestmark = pytest.mark.django_db

ROW = {
    "comicvine_id": 10,
    "comicvine_url": "https://cv/i10",
    "name": "N",
    "number": "1",
    "cover_date": "2020-01-31",
    "volume_comicvine_id": 100,
    "volume_comicvine_url": "https://cv/v100",
    "volume_name": "Vol",
    "volume_start_year": 1940,
    "publisher_name": "Pub",
    "publisher_comicvine_id": 500,
    "publisher_comicvine_url": "https://cv/p500",
}
STORED = dict(ROW, cover_date=date(2020, 1, 31), volume_start_year="1940", numerical_number=1.0)
plan = character_missing_issues_task.build_write_plan


def test_plan_creates_new_row():
    result = plan([dict(ROW)])
    [mi] = result["create"]
    assert (mi.comicvine_id, mi.cover_date, mi.volume_start_year, mi.numerical_number) == (
        10,
        date(2020, 1, 31),
        "1940",
        1.0,
    )
    assert mi.pk is None
    assert result["update"] == [] and result["skip_reset_ids"] == []


def test_plan_new_row_without_cover_date_has_none():
    [mi] = plan([dict(ROW, cover_date=None)])["create"]
    assert mi.cover_date is None


def test_plan_skips_unchanged_row():
    MissingIssue.objects.create(**STORED)
    assert plan([dict(ROW)]) == {"create": [], "update": [], "skip_reset_ids": []}


def test_plan_updates_changed_row():
    MissingIssue.objects.create(**dict(STORED, name="Old"))
    [mi] = plan([dict(ROW)])["update"]
    assert mi.name == "N"


def test_plan_recomputes_numerical_number():
    MissingIssue.objects.create(**dict(STORED, numerical_number=5.0))
    [mi] = plan([dict(ROW)])["update"]
    assert mi.numerical_number == 1.0


def test_plan_overwrites_absent_fields_with_none():
    MissingIssue.objects.create(**STORED)
    [mi] = plan([dict(ROW, publisher_name=None, publisher_comicvine_id=None)])["update"]
    assert (mi.publisher_name, mi.publisher_comicvine_id) == (None, None)


def test_plan_keeps_cover_date_when_mongo_has_none():
    MissingIssue.objects.create(**dict(STORED, cover_date=date(2019, 12, 1), name="Old"))
    [mi] = plan([dict(ROW, cover_date=None)])["update"]
    assert mi.cover_date == date(2019, 12, 1)
    assert plan([dict(ROW, cover_date=None, name="Old")])["update"] == []


def test_plan_does_not_mutate_rows_or_skip():
    MissingIssue.objects.create(**dict(STORED, name="Old", skip=True, skip_date=date.today() - timedelta(days=100)))
    rows = [dict(ROW)]
    [mi] = plan(rows)["update"]
    assert rows == [ROW]
    assert mi.skip is True and mi.skip_date == date.today() - timedelta(days=100)


def test_plan_skip_reset_ids(settings):
    settings.SKIP_DAYS = 7
    today = date.today()
    MissingIssue.objects.create(**dict(STORED, comicvine_id=1, skip=True, skip_date=today - timedelta(days=8)))
    MissingIssue.objects.create(**dict(STORED, comicvine_id=2, skip=True, skip_date=today - timedelta(days=1)))
    MissingIssue.objects.create(**dict(STORED, comicvine_id=3))
    rows = [dict(ROW, comicvine_id=i) for i in (1, 2, 3)]
    assert plan(rows)["skip_reset_ids"] == [1]


def test_plan_reads_existing_rows_with_one_query(django_assert_num_queries):
    MissingIssue.objects.create(**STORED)
    with django_assert_num_queries(1):
        plan([dict(ROW), dict(ROW, comicvine_id=11)])
