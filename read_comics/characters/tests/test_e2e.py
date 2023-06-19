from datetime import date

import pytest
from django.db.models import Count
from rest_framework.test import APIClient
from utils.utils import flatten_dict

from ..models import Character

pytestmark = pytest.mark.django_db


class TestCharactersCount:
    @staticmethod
    def test_no_show_all(
        api_client: APIClient, characters_no_issues: list[Character], characters_with_issues: list[Character]
    ) -> None:
        response = api_client.get("/api/characters/count/")
        assert response.status_code == 200
        assert response.data["count"] == len(characters_with_issues)

    @staticmethod
    def test_show_all(
        api_client: APIClient, characters_no_issues: list[Character], characters_with_issues: list[Character]
    ) -> None:
        response = api_client.get("/api/characters/count/?show-all=yes")
        assert response.status_code == 200
        assert response.data["count"] == len(characters_with_issues) + len(characters_no_issues)


class TestCharactersList:
    list_keys = {
        "slug",
        "image",
        "publisher__name",
        "publisher__image",
        "publisher__slug",
        "name",
        "short_description",
        "issues_count",
        "volumes_count",
    }

    def test_no_show_all(
        self, api_client: APIClient, characters_no_issues: list[Character], characters_with_issues: list[Character]
    ) -> None:
        response = api_client.get("/api/characters/")

        assert response.status_code == 200
        assert response.data["count"] == len(characters_with_issues)

        flatten_response_data = [flatten_dict(response_item) for response_item in response.data["results"]]
        for item in flatten_response_data:
            assert self.list_keys == set(item.keys())

    def test_show_all(
        self, api_client: APIClient, characters_no_issues: list[Character], characters_with_issues: list[Character]
    ) -> None:
        response = api_client.get("/api/characters/?show-all=yes")

        assert response.status_code == 200
        assert response.data["count"] == len(characters_no_issues) + len(characters_with_issues)

        flatten_response_data = [flatten_dict(response_item) for response_item in response.data["results"]]
        for item in flatten_response_data:
            assert self.list_keys == set(item.keys())

    @staticmethod
    def test_data(api_client: APIClient, character_with_issues: Character) -> None:
        response = api_client.get("/api/characters/")

        assert response.status_code == 200
        assert response.data["count"] == 1

        response_data = response.data["results"][0]
        assert response_data["slug"] == character_with_issues.slug
        assert response_data["name"] == character_with_issues.name
        assert response_data["publisher"]["name"] == (
            character_with_issues.publisher.name if character_with_issues.publisher else None
        )
        assert response_data["publisher"]["slug"] == (
            character_with_issues.publisher.slug if character_with_issues.publisher else None
        )
        assert response_data["short_description"] == character_with_issues.short_description
        assert response_data["issues_count"] == character_with_issues.issues.count()
        assert (
            response_data["volumes_count"]
            == character_with_issues.issues.aggregate(v=Count("volume", distinct=True))["v"]
        )


class TestCharacterDetail:
    @staticmethod
    def test_with_first_issue(api_client: APIClient, character_with_issues: Character) -> None:
        response = api_client.get(f"/api/characters/{character_with_issues.slug}/")

        assert response.status_code == 200

        assert response.data["slug"] == character_with_issues.slug
        assert response.data["name"] == character_with_issues.name
        assert response.data["real_name"] == character_with_issues.real_name
        assert response.data["publisher"]["name"] == (
            character_with_issues.publisher.name if character_with_issues.publisher is not None else None
        )
        assert response.data["publisher"]["slug"] == (
            character_with_issues.publisher.slug if character_with_issues.publisher is not None else None
        )
        assert response.data["aliases"] == character_with_issues.get_aliases_list()
        assert date.fromisoformat(response.data["birth"]) == character_with_issues.birth
        assert response.data["gender"] == character_with_issues.get_gender_display()
        assert set(response.data["powers"]) == set(map(lambda x: x.name, character_with_issues.powers.all()))
        assert response.data["first_issue_name"] == (
            character_with_issues.first_issue.display_name if character_with_issues.first_issue is not None else None
        )
        assert response.data["first_issue_slug"] == (
            character_with_issues.first_issue.slug if character_with_issues.first_issue is not None else None
        )
        assert response.data["comicvine_url"] == character_with_issues.comicvine_url
        assert response.data["short_description"] == character_with_issues.short_description
        assert response.data["description"] == character_with_issues.description
        assert response.data["download_size"] == character_with_issues.download_size
        assert response.data["download_link"] == f"http://testserver{character_with_issues.download_link}"

    @staticmethod
    def test_no_first_issue(api_client: APIClient, character_no_issues: Character) -> None:
        response = api_client.get(f"/api/characters/{character_no_issues.slug}/")

        assert response.status_code == 200

        assert response.data["first_issue_name"] == character_no_issues.first_issue_name
        assert response.data["first_issue_slug"] is None
        assert response.data["download_size"] == "0\xa0bytes"


class TestCharacterTechnicalInfo:
    @staticmethod
    def test_no_auth(api_client: APIClient, character_no_issues: Character) -> None:
        response = api_client.get(f"/api/characters/{character_no_issues.slug}/technical-info/")

        assert response.status_code == 401

    @staticmethod
    def test_regular_user(authenticated_api_client: APIClient, character_no_issues: Character) -> None:
        response = authenticated_api_client.get(f"/api/characters/{character_no_issues.slug}/technical-info/")

        assert response.status_code == 403

    @staticmethod
    def test_staff(staff_api_client: APIClient, character_no_issues: Character) -> None:
        response = staff_api_client.get(f"/api/characters/{character_no_issues.slug}/technical-info/")

        assert response.status_code == 200

    @staticmethod
    def test_superuser(superuser_api_client: APIClient, character_no_issues: Character) -> None:
        response = superuser_api_client.get(f"/api/characters/{character_no_issues.slug}/technical-info/")

        assert response.status_code == 200

        assert response.data["id"] == character_no_issues.id
        assert response.data["comicvine_id"] == character_no_issues.comicvine_id
        assert response.data["comicvine_status"] == character_no_issues.get_comicvine_status_display()
        assert response.data["comicvine_last_match"] == character_no_issues.comicvine_last_match.strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
        assert response.data["created_dt"] == character_no_issues.created_dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        assert response.data["modified_dt"] == character_no_issues.modified_dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
