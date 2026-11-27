from datetime import date
from urllib.parse import parse_qs, urlsplit

import pytest
from django.urls import reverse

from read_comics.missing_issues.models import MissingIssue
from read_comics.missing_issues.skip import get_skip_until


@pytest.mark.parametrize(
    ("scope", "expected"),
    [("issue", {10}), ("volume", {10, 11}), ("publisher", {10, 11, 12})],
)
@pytest.mark.django_db
def test_skip_scope(staff_client, monkeypatch, scope, expected):
    monkeypatch.setattr("django.utils.timezone.localdate", lambda: date(2026, 3, 1))
    for cid, volume, publisher in [(10, 1, 1), (11, 1, 1), (12, 2, 1), (13, 3, 2)]:
        MissingIssue.objects.create(
            comicvine_id=cid,
            volume_comicvine_id=volume,
            publisher_comicvine_id=publisher,
            skip_until=date(2027, 3, 1) if cid == 11 else None,
        )
    url = reverse(f"missing_issues:skip_{scope}", args=[10])
    assert staff_client.get(url, {"duration": "bad"}).status_code == 400
    assert staff_client.get(url).status_code == 400
    assert MissingIssue.objects.get(comicvine_id=10).skip_until is None
    response = staff_client.get(url, {"duration": "7d", "page": 2, "q": "A&B"})
    assert response.status_code == 302
    assert parse_qs(urlsplit(response.url).query) == {"page": ["2"], "q": ["A&B"], "response_type": ["partial"]}
    assert MissingIssue.objects.get(comicvine_id=11).skip_until == (
        date(2026, 3, 8) if 11 in expected else date(2027, 3, 1)
    )
    assert (
        MissingIssue.objects.create(comicvine_id=14, volume_comicvine_id=1, publisher_comicvine_id=1).skip_until is None
    )
    assert (
        set(MissingIssue.objects.filter(skip_until=date(2026, 3, 8)).values_list("comicvine_id", flat=True)) == expected
    )


@pytest.mark.django_db
def test_visible_on_return_date():
    for cid, until in [(10, None), (11, date(2026, 3, 7)), (12, date(2026, 3, 8)), (13, date(2026, 3, 9))]:
        MissingIssue.objects.create(comicvine_id=cid, skip_until=until)
    assert set(MissingIssue.objects.visible(date(2026, 3, 8)).values_list("comicvine_id", flat=True)) == {10, 11, 12}


@pytest.mark.parametrize(
    ("duration", "today", "expected"),
    [
        ("7d", date(2026, 3, 1), date(2026, 3, 8)),
        ("30d", date(2026, 3, 1), date(2026, 3, 31)),
        ("6m", date(2026, 8, 31), date(2027, 2, 28)),
        ("1y", date(2028, 2, 29), date(2029, 2, 28)),
    ],
)
def test_skip_duration_dates(duration, today, expected):
    assert get_skip_until(duration, today) == expected
