import pytest
from django.urls import reverse

from read_comics.missing_issues.models import MissingIssue

pytestmark = pytest.mark.django_db


def test_category_ignore_publisher_button(staff_client, character):
    issue = MissingIssue.objects.create(
        comicvine_id=10, volume_name="Vol", volume_comicvine_id=100, publisher_comicvine_id=500
    )
    issue.characters.add(character)
    kwargs = {"category": "character", "slug": character.slug}
    content = staff_client.get(
        reverse("missing_issues:category", kwargs=kwargs), {"response_type": "partial"}
    ).content.decode()
    assert reverse("missing_issues:category_ignore_publisher", kwargs={**kwargs, "comicvine_id": 10}) in content


def test_details_buttons(staff_client):
    MissingIssue.objects.create(comicvine_id=10, volume_name="Vol", volume_comicvine_id=100, publisher_comicvine_id=500)
    MissingIssue.objects.create(comicvine_id=20, volume_name="Orphan")
    content = staff_client.get(reverse("missing_issues:all"), {"response_type": "partial"}).content.decode()
    for level, cid in (("publisher", 500), ("volume", 100), ("issue", 10), ("issue", 20)):
        assert reverse("missing_issues:comicvine_details", kwargs={"level": level, "comicvine_id": cid}) in content
    assert content.count("btn-comicvine-details") == 4


@pytest.mark.parametrize("listing", ["all", "category", "watched"])
def test_skip_duration_menu(staff_client, staff_user, character, listing):
    issue = MissingIssue.objects.create(
        comicvine_id=10, name="A&B", volume_comicvine_id=100, publisher_comicvine_id=500
    )
    issue.characters.add(character)
    if listing == "watched":
        character.watchers.create(user=staff_user)
    category = {"category": "character", "slug": character.slug} if listing == "category" else {}
    content = staff_client.get(
        reverse(f"missing_issues:{listing}", kwargs=category), {"response_type": "partial", "q": "A&B"}
    ).content.decode()
    prefix = "" if listing == "all" else f"{listing}_"
    for scope in ("issue", "volume", "publisher"):
        action = reverse(f"missing_issues:{prefix}skip_{scope}", kwargs={**category, "comicvine_id": 10})
        for code in ("7d", "30d", "6m", "1y"):
            assert f"{action}?duration={code}&amp;page=1&amp;q=A%26B" in content
