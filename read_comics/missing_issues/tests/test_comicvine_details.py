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


def test_cover_sort_key():
    docs = [
        {"id": 1, "issue_number": "10"},
        {"id": 2, "issue_number": None},
        {"id": 3, "issue_number": "2"},
        {"id": 4, "issue_number": "½"},
        {"id": 5, "issue_number": "1A"},
        {"id": 6, "issue_number": "A"},
        {"id": 7, "issue_number": ""},
    ]
    assert [d["id"] for d in sorted(docs, key=ComicvineDetailsView.cover_sort_key)] == [6, 4, 5, 3, 1, 2, 7]


def test_volume(staff_client, cv_volumes, cv_issues):
    cv_volumes.insert_one(
        {
            "id": 100,
            "name": "Fictional Tales",
            "start_year": "1999",
            "publisher": {"id": 500, "name": "Fictional Press"},
            "first_issue": {"issue_number": "1"},
            "last_issue": {"issue_number": "3"},
            "aliases": "FT",
            "deck": "Tales",
            "description": "<p>About</p>",
            "crawl_source": "detail",
        }
    )
    cv_issues.insert_many(
        [
            {
                "id": 12,
                "volume": {"id": 100},
                "issue_number": "2",
                "cover_date": "1999-02-01",
                "image": {"small_url": "https://img/s2.jpg", "original_url": "https://img/o2.jpg"},
            },
            {
                "id": 11,
                "volume": {"id": 100},
                "issue_number": "1",
                "cover_date": "1999-01-01",
                "image": {"small_url": "https://img/s1.jpg", "original_url": "https://img/o1.jpg"},
            },
            {"id": 13, "volume": {"id": 100}, "issue_number": "3", "image": None},
            {
                "id": 99,
                "volume": {"id": 101},
                "issue_number": "1",
                "image": {"small_url": "https://img/s99.jpg", "original_url": "https://img/o99.jpg"},
            },
        ]
    )
    response = staff_client.get(url("volume", 100))
    content = response.content.decode()
    assert response.context["issues_count"] == 3
    assert [c.number for c in response.context["covers"]] == ["1", "2", "3"]
    for text in (
        "Fictional Tales (1999)",
        "Fictional Press",
        "#1",
        "#3",
        'href="https://img/o1.jpg"',
        'loading="lazy"',
        'width="412"',
        'height="640"',
        "No cover",
    ):
        assert text in content
    assert content.index("https://img/s1.jpg") < content.index("https://img/s2.jpg")
    assert "https://img/s99.jpg" not in content


def test_volume_without_issues(staff_client, cv_volumes):
    cv_volumes.insert_one({"id": 102, "name": "Empty Tales"})
    response = staff_client.get(url("volume", 102))
    assert response.context["issues_count"] == 0 and response.context["covers"] == []


def test_volume_issues_with_empty_number_and_image(staff_client, cv_volumes, cv_issues):
    cv_volumes.insert_one({"id": 103, "name": "Odd Tales"})
    cv_issues.insert_many(
        [
            {"id": 31, "volume": {"id": 103}, "issue_number": None},
            {"id": 32, "volume": {"id": 103}, "issue_number": "", "image": None},
            {"id": 33, "volume": {"id": 103}, "issue_number": "1", "image": {"small_url": None, "original_url": None}},
        ]
    )
    response = staff_client.get(url("volume", 103))
    covers = response.context["covers"]
    assert [c.number for c in covers] == ["1", None, ""]
    assert all(c.image_url is None and c.full_url is None for c in covers)
    assert response.content.decode().count("No cover") == 3
