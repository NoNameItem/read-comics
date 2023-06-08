import pytest
from utils.utils import flatten_dict

from ..models import Character

pytestmark = pytest.mark.django_db


class TestCharactersE2E:
    list_keys = {
        "slug",
        "image",
        "publisher__name",
        "publisher__image",
        "name",
        "short_description",
        "issues_count",
        "volumes_count",
    }

    # Count tests
    ##########################

    @staticmethod
    def test_count(api_client, characters_no_issues, characters_with_issues) -> None:
        response = api_client().get("/api/characters/count/")
        assert response.status_code == 200
        assert response.data["count"] == len(characters_with_issues)

    @staticmethod
    def test_count_all(api_client, characters_no_issues, characters_with_issues) -> None:
        response = api_client().get("/api/characters/count/?show-all=yes")
        assert response.status_code == 200
        assert response.data["count"] == len(characters_with_issues) + len(characters_no_issues)

    # List tests
    ##########################

    def test_list(self, api_client, characters_no_issues, characters_with_issues) -> None:
        response = api_client().get("/api/characters/")

        assert response.status_code == 200
        assert response.data["count"] == len(characters_with_issues)

        flatten_response_data = [flatten_dict(response_item) for response_item in response.data["results"]]
        for item in flatten_response_data:
            assert self.list_keys == set(item.keys())

    def test_list_show_all(self, api_client, characters_no_issues, characters_with_issues) -> None:
        response = api_client().get("/api/characters/?show-all=yes")

        assert response.status_code == 200
        assert response.data["count"] == len(characters_no_issues) + len(characters_with_issues)

        flatten_response_data = [flatten_dict(response_item) for response_item in response.data["results"]]
        for item in flatten_response_data:
            assert self.list_keys == set(item.keys())

    @staticmethod
    def test_list_data(api_client, character_with_issues: Character):
        response = api_client().get("/api/characters/")

        assert response.status_code == 200
        assert response.data["count"] == 1

        response_data = response.data["results"][0]
        assert response_data["slug"] == character_with_issues.slug
        assert response_data["publisher"]["name"] == (
            character_with_issues.publisher.name if character_with_issues.publisher else None
        )
        assert response_data["short_description"] == character_with_issues.short_description
        assert response_data["issues_count"] == character_with_issues.issues.count()
