from datetime import datetime

import pytest
from django.urls import reverse

from read_comics.missing_issues.views import ComicvineDetailsView
from read_comics.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db

Field = ComicvineDetailsView.Field


def url(level, comicvine_id):
    return reverse("missing_issues:comicvine_details", kwargs={"level": level, "comicvine_id": comicvine_id})


def test_make_field():
    doc = {"a": None, "b": "", "c": [], "d": "x"}
    make_field = ComicvineDetailsView.make_field
    assert make_field(doc, "z") == Field("missing", None)
    assert all(make_field(doc, k) == Field("empty", None) for k in "abc")
    assert make_field(doc, "d", str.upper) == Field("value", "X")
    assert make_field(doc, "d", lambda value: []) == Field("empty", None)


def test_unknown_level(staff_client, cv_db):
    assert staff_client.get(url("story_arc", 1)).status_code == 404


def test_non_staff(client, cv_db):
    client.force_login(UserFactory())
    assert client.get(url("publisher", 1)).status_code == 403


def test_no_document(staff_client, cv_db):
    response = staff_client.get(url("publisher", 404))
    assert response.status_code == 200
    assert "No data for this object in our database yet" in response.content.decode()


def test_publisher(staff_client, cv_publishers):
    cv_publishers.insert_one(
        {
            "id": 500,
            "name": "Fictional Press",
            "aliases": "FP\r\nFict Press",
            "deck": "Small press",
            "description": '<p>Founded by <a href="https://cv/p">Jane Roe</a>.</p>'
            '<img class="js-lazy-load-image" data-src="https://img/p.jpg"/>',
            "site_detail_url": "https://cv/p500",
            "crawl_date": datetime(2026, 10, 5, 12, 0),
            "crawl_source": "detail",
        }
    )
    content = staff_client.get(url("publisher", 500)).content.decode()
    for text in (
        "Fictional Press",
        "<li>FP</li>",
        "<li>Fict Press</li>",
        "Small press",
        "Founded by Jane Roe.",
        'src="https://img/p.jpg"',
        "Data as of 2026-10-05",
        'href="https://cv/p500"',
    ):
        assert text in content
    assert 'href="https://cv/p"' not in content and "Only list data" not in content


def test_list_only_document(staff_client, cv_publishers):
    cv_publishers.insert_one({"id": 501, "name": "List Press", "deck": None, "crawl_source": "list"})
    response = staff_client.get(url("publisher", 501))
    assert "Only list data downloaded so far, details are not crawled yet" in response.content.decode()
    fields = response.context["fields"]
    assert fields["aliases"] == fields["description"] == Field("missing", None)
    assert fields["deck"] == Field("empty", None)
    assert 'text-muted">none<' in response.content.decode()


def test_footer_without_date_and_url(staff_client, cv_publishers):
    cv_publishers.insert_one({"id": 502, "name": "Bare Press"})
    content = staff_client.get(url("publisher", 502)).content.decode()
    assert "Data as of" not in content and "Open on ComicVine" not in content
