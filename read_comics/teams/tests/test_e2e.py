import pytest
from django.db.models import Count
from rest_framework.test import APIClient
from utils.utils import flatten_dict

from ..models import Team

pytestmark = pytest.mark.django_db


class TestTeamsE2E:
    @staticmethod
    def test_count(api_client: APIClient, teams_no_issues: list[Team], teams_with_issues: list[Team]) -> None:
        response = api_client.get("/api/teams/count/")
        assert response.status_code == 200
        assert response.data["count"] == len(teams_with_issues)

    @staticmethod
    def test_count_all(api_client: APIClient, teams_no_issues: list[Team], teams_with_issues: list[Team]) -> None:
        response = api_client.get("/api/teams/count/?show-all=yes")
        assert response.status_code == 200
        assert response.data["count"] == len(teams_with_issues) + len(teams_no_issues)


class TestTeamsList:
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
        self, api_client: APIClient, teams_no_issues: list[Team], teams_with_issues: list[Team]
    ) -> None:
        response = api_client.get("/api/teams/")

        assert response.status_code == 200
        assert response.data["count"] == len(teams_with_issues)

        flatten_response_data = [flatten_dict(response_item) for response_item in response.data["results"]]
        for item in flatten_response_data:
            assert self.list_keys == set(item.keys())

    def test_show_all(self, api_client: APIClient, teams_no_issues: list[Team], teams_with_issues: list[Team]) -> None:
        response = api_client.get("/api/teams/?show-all=yes")

        assert response.status_code == 200
        assert response.data["count"] == len(teams_no_issues) + len(teams_with_issues)

        flatten_response_data = [flatten_dict(response_item) for response_item in response.data["results"]]
        for item in flatten_response_data:
            assert self.list_keys == set(item.keys())

    @staticmethod
    def test_data(api_client: APIClient, team_with_issues: Team) -> None:
        response = api_client.get("/api/teams/")

        assert response.status_code == 200
        assert response.data["count"] == 1

        response_data = response.data["results"][0]
        assert response_data["slug"] == team_with_issues.slug
        assert response_data["name"] == team_with_issues.name
        assert response_data["publisher"]["name"] == (
            team_with_issues.publisher.name if team_with_issues.publisher else None
        )
        assert response_data["publisher"]["slug"] == (
            team_with_issues.publisher.slug if team_with_issues.publisher else None
        )
        assert response_data["short_description"] == team_with_issues.short_description
        assert response_data["issues_count"] == team_with_issues.issues.count()
        assert (
            response_data["volumes_count"] == team_with_issues.issues.aggregate(v=Count("volume", distinct=True))["v"]
        )
