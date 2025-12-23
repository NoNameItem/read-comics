# Docs: [[docs/backend/teams/testing/test_e2e.md]]
import pytest
from django.db.models import Count
from rest_framework.test import APIClient
from utils.utils import flatten_dict

from ..models import Team

pytestmark = pytest.mark.django_db


class TestTeamsCount:
    @staticmethod
    def test_no_show_all(api_client: APIClient, teams_no_issues: list[Team], teams_with_issues: list[Team]) -> None:
        response = api_client.get("/api/teams/count/")
        assert response.status_code == 200
        assert response.data["count"] == len(teams_with_issues)

    @staticmethod
    def test_show_all(api_client: APIClient, teams_no_issues: list[Team], teams_with_issues: list[Team]) -> None:
        response = api_client.get("/api/teams/count/?show-all=yes")
        assert response.status_code == 200
        assert response.data["count"] == len(teams_with_issues) + len(teams_no_issues)

    @staticmethod
    def test_empty_database(api_client: APIClient) -> None:
        response = api_client.get("/api/teams/count/")
        assert response.status_code == 200
        assert response.data["count"] == 0

    @staticmethod
    def test_only_teams_without_issues(api_client: APIClient, teams_no_issues: list[Team]) -> None:
        response = api_client.get("/api/teams/count/")
        assert response.status_code == 200
        assert response.data["count"] == 0


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

    @staticmethod
    def test_empty_database(api_client: APIClient) -> None:
        response = api_client.get("/api/teams/")

        assert response.status_code == 200
        assert response.data["count"] == 0
        assert response.data["results"] == []

    @staticmethod
    def test_only_teams_without_issues(api_client: APIClient, teams_no_issues: list[Team]) -> None:
        response = api_client.get("/api/teams/")

        assert response.status_code == 200
        assert response.data["count"] == 0
        assert response.data["results"] == []

    @staticmethod
    def test_team_without_publisher(api_client: APIClient, team_with_issues: Team) -> None:
        team_with_issues.publisher = None
        team_with_issues.save()

        response = api_client.get("/api/teams/")

        assert response.status_code == 200
        assert response.data["count"] == 1

        response_data = response.data["results"][0]
        assert response_data["publisher"] is None

    @staticmethod
    def test_default_ordering_by_name(api_client: APIClient, teams_with_issues: list[Team]) -> None:
        response = api_client.get("/api/teams/")

        assert response.status_code == 200
        assert response.data["count"] == len(teams_with_issues)

        names = [item["name"] for item in response.data["results"]]
        assert names == sorted(names)

    @staticmethod
    def test_ordering_by_name_ascending(api_client: APIClient, teams_with_issues: list[Team]) -> None:
        response = api_client.get("/api/teams/?ordering=name")

        assert response.status_code == 200
        names = [item["name"] for item in response.data["results"]]
        assert names == sorted(names)

    @staticmethod
    def test_ordering_by_name_descending(api_client: APIClient, teams_with_issues: list[Team]) -> None:
        response = api_client.get("/api/teams/?ordering=-name")

        assert response.status_code == 200
        names = [item["name"] for item in response.data["results"]]
        assert names == sorted(names, reverse=True)

    @staticmethod
    def test_ordering_by_issues_count_ascending(api_client: APIClient, teams_with_issues: list[Team]) -> None:
        response = api_client.get("/api/teams/?ordering=issues_count")

        assert response.status_code == 200
        issues_counts = [item["issues_count"] for item in response.data["results"]]
        assert issues_counts == sorted(issues_counts)

    @staticmethod
    def test_ordering_by_issues_count_descending(api_client: APIClient, teams_with_issues: list[Team]) -> None:
        response = api_client.get("/api/teams/?ordering=-issues_count")

        assert response.status_code == 200
        issues_counts = [item["issues_count"] for item in response.data["results"]]
        assert issues_counts == sorted(issues_counts, reverse=True)

    @staticmethod
    def test_ordering_by_volumes_count_ascending(api_client: APIClient, teams_with_issues: list[Team]) -> None:
        response = api_client.get("/api/teams/?ordering=volumes_count")

        assert response.status_code == 200
        volumes_counts = [item["volumes_count"] for item in response.data["results"]]
        assert volumes_counts == sorted(volumes_counts)

    @staticmethod
    def test_ordering_by_volumes_count_descending(api_client: APIClient, teams_with_issues: list[Team]) -> None:
        response = api_client.get("/api/teams/?ordering=-volumes_count")

        assert response.status_code == 200
        volumes_counts = [item["volumes_count"] for item in response.data["results"]]
        assert volumes_counts == sorted(volumes_counts, reverse=True)

    @staticmethod
    def test_invalid_ordering_field(api_client: APIClient, teams_with_issues: list[Team]) -> None:
        response = api_client.get("/api/teams/?ordering=invalid_field")

        assert response.status_code == 200
        # Should fall back to default ordering (name)
        names = [item["name"] for item in response.data["results"]]
        assert names == sorted(names)

    @staticmethod
    def test_pagination_first_page(api_client: APIClient, teams_with_issues: list[Team]) -> None:
        response = api_client.get("/api/teams/?page=1")

        assert response.status_code == 200
        assert "count" in response.data
        assert "next" in response.data
        assert "previous" in response.data
        assert "results" in response.data

    @staticmethod
    def test_pagination_invalid_page(api_client: APIClient, teams_with_issues: list[Team]) -> None:
        response = api_client.get("/api/teams/?page=999")

        assert response.status_code == 404

    @staticmethod
    def test_multiple_filters_combined(
        api_client: APIClient, teams_no_issues: list[Team], teams_with_issues: list[Team]
    ) -> None:
        response = api_client.get("/api/teams/?show-all=yes&ordering=-name")

        assert response.status_code == 200
        assert response.data["count"] == len(teams_with_issues) + len(teams_no_issues)

        names = [item["name"] for item in response.data["results"]]
        assert names == sorted(names, reverse=True)


class TestTeamsParametrized:
    @pytest.mark.parametrize("ordering,is_reverse", [("name", False), ("-name", True), ("issues_count", False)])
    def test_ordering_parametrized(self, api_client: APIClient, teams_with_issues: list[Team], ordering: str, is_reverse: bool) -> None:
        response = api_client.get(f"/api/teams/?ordering={ordering}")
        assert response.status_code == 200
        field = ordering.lstrip("-")
        values = [item[field] for item in response.data["results"]]
        assert values == sorted(values, reverse=is_reverse)


class TestTeamsEdgeCases:
    @staticmethod
    def test_pagination_boundary_first_page(api_client: APIClient, teams_with_issues: list[Team]) -> None:
        response = api_client.get("/api/teams/?page=1")
        assert response.status_code == 200

    @staticmethod
    def test_list_with_large_page_size(api_client: APIClient, teams_with_issues: list[Team]) -> None:
        response = api_client.get("/api/teams/?page_size=10000")
        assert response.status_code == 200


class TestTeamsConsistency:
    @staticmethod
    def test_count_vs_list_consistency(api_client: APIClient, teams_with_issues: list[Team]) -> None:
        assert api_client.get("/api/teams/").data["count"] == api_client.get("/api/teams/count/").data["count"]

    @staticmethod
    def test_count_with_show_all_consistency(api_client: APIClient, teams_with_issues: list[Team], teams_no_issues: list[Team]) -> None:
        list_resp = api_client.get("/api/teams/?show-all=yes")
        count_resp = api_client.get("/api/teams/count/?show-all=yes")
        assert list_resp.data["count"] == count_resp.data["count"]


class TestTeamsHTTPMethods:
    @staticmethod
    def test_list_endpoint_rejects_post(api_client: APIClient) -> None:
        response = api_client.post("/api/teams/", {"name": "New"})
        assert response.status_code in [405, 403, 400]

    @staticmethod
    def test_detail_endpoint_rejects_patch(api_client: APIClient, team_with_issues: Team) -> None:
        response = api_client.patch(f"/api/teams/{team_with_issues.slug}/", {"name": "Updated"})
        assert response.status_code in [405, 403, 400]
