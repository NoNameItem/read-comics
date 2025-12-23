# Docs: [[docs/backend/people/testing/test_e2e.md]]
import pytest
from django.db.models import Count
from rest_framework.test import APIClient
from utils.utils import flatten_dict

from ..models import Person

pytestmark = pytest.mark.django_db


class TestPeopleCount:
    # Count tests
    ##########################

    @staticmethod
    def test_count(api_client: APIClient, people_no_issues: list[Person], people_with_issues: list[Person]) -> None:
        response = api_client.get("/api/people/count/")
        assert response.status_code == 200
        assert response.data["count"] == len(people_with_issues)

    @staticmethod
    def test_count_all(api_client: APIClient, people_no_issues: list[Person], people_with_issues: list[Person]) -> None:
        response = api_client.get("/api/people/count/?show-all=yes")
        assert response.status_code == 200
        assert response.data["count"] == len(people_with_issues) + len(people_no_issues)

    @staticmethod
    def test_empty_database(api_client: APIClient) -> None:
        response = api_client.get("/api/people/count/")
        assert response.status_code == 200
        assert response.data["count"] == 0


class TestPeopleList:
    list_keys = {"slug", "image", "name", "short_description", "issues_count", "volumes_count"}

    def test_no_show_all(
        self, api_client: APIClient, people_no_issues: list[Person], people_with_issues: list[Person]
    ) -> None:
        response = api_client.get("/api/people/")

        assert response.status_code == 200
        assert response.data["count"] == len(people_with_issues)

        flatten_response_data = [flatten_dict(response_item) for response_item in response.data["results"]]
        for item in flatten_response_data:
            assert self.list_keys == set(item.keys())

    def test_show_all(
        self, api_client: APIClient, people_no_issues: list[Person], people_with_issues: list[Person]
    ) -> None:
        response = api_client.get("/api/people/?show-all=yes")

        assert response.status_code == 200
        assert response.data["count"] == len(people_no_issues) + len(people_with_issues)

        flatten_response_data = [flatten_dict(response_item) for response_item in response.data["results"]]
        for item in flatten_response_data:
            assert self.list_keys == set(item.keys())

    @staticmethod
    def test_data(api_client: APIClient, person_with_issues: Person):
        response = api_client.get("/api/people/")

        assert response.status_code == 200
        assert response.data["count"] == 1

        response_data = response.data["results"][0]
        assert response_data["slug"] == person_with_issues.slug
        assert response_data["name"] == person_with_issues.name
        assert response_data["short_description"] == person_with_issues.short_description
        assert response_data["issues_count"] == person_with_issues.issues.count()
        assert (
            response_data["volumes_count"] == person_with_issues.issues.aggregate(v=Count("volume", distinct=True))["v"]
        )

    @staticmethod
    def test_empty_database(api_client: APIClient) -> None:
        response = api_client.get("/api/people/")
        assert response.status_code == 200
        assert response.data["count"] == 0
        assert response.data["results"] == []

    @staticmethod
    def test_default_ordering_by_name(api_client: APIClient, people_with_issues: list[Person]) -> None:
        response = api_client.get("/api/people/")

        assert response.status_code == 200
        assert response.data["count"] == len(people_with_issues)

        names = [item["name"] for item in response.data["results"]]
        assert names == sorted(names)

    @staticmethod
    def test_ordering_by_name_ascending(api_client: APIClient, people_with_issues: list[Person]) -> None:
        response = api_client.get("/api/people/?ordering=name")

        assert response.status_code == 200
        names = [item["name"] for item in response.data["results"]]
        assert names == sorted(names)

    @staticmethod
    def test_ordering_by_name_descending(api_client: APIClient, people_with_issues: list[Person]) -> None:
        response = api_client.get("/api/people/?ordering=-name")

        assert response.status_code == 200
        names = [item["name"] for item in response.data["results"]]
        assert names == sorted(names, reverse=True)

    @staticmethod
    def test_ordering_by_issues_count_ascending(api_client: APIClient, people_with_issues: list[Person]) -> None:
        response = api_client.get("/api/people/?ordering=issues_count")

        assert response.status_code == 200
        issues_counts = [item["issues_count"] for item in response.data["results"]]
        assert issues_counts == sorted(issues_counts)

    @staticmethod
    def test_ordering_by_issues_count_descending(api_client: APIClient, people_with_issues: list[Person]) -> None:
        response = api_client.get("/api/people/?ordering=-issues_count")

        assert response.status_code == 200
        issues_counts = [item["issues_count"] for item in response.data["results"]]
        assert issues_counts == sorted(issues_counts, reverse=True)

    @staticmethod
    def test_ordering_by_volumes_count_ascending(api_client: APIClient, people_with_issues: list[Person]) -> None:
        response = api_client.get("/api/people/?ordering=volumes_count")

        assert response.status_code == 200
        volumes_counts = [item["volumes_count"] for item in response.data["results"]]
        assert volumes_counts == sorted(volumes_counts)

    @staticmethod
    def test_ordering_by_volumes_count_descending(api_client: APIClient, people_with_issues: list[Person]) -> None:
        response = api_client.get("/api/people/?ordering=-volumes_count")

        assert response.status_code == 200
        volumes_counts = [item["volumes_count"] for item in response.data["results"]]
        assert volumes_counts == sorted(volumes_counts, reverse=True)

    @staticmethod
    def test_invalid_ordering_field(api_client: APIClient, people_with_issues: list[Person]) -> None:
        response = api_client.get("/api/people/?ordering=invalid_field")

        assert response.status_code == 200
        names = [item["name"] for item in response.data["results"]]
        assert names == sorted(names)

    @staticmethod
    def test_pagination_invalid_page(api_client: APIClient, people_with_issues: list[Person]) -> None:
        response = api_client.get("/api/people/?page=999")

        assert response.status_code == 404


class TestPeopleParametrized:
    @pytest.mark.parametrize("ordering,is_reverse", [("name", False), ("-name", True)])
    def test_ordering_parametrized(self, api_client: APIClient, people_with_issues: list[Person], ordering: str, is_reverse: bool) -> None:
        response = api_client.get(f"/api/people/?ordering={ordering}")
        assert response.status_code == 200
        values = [item[ordering.lstrip("-")] for item in response.data["results"]]
        assert values == sorted(values, reverse=is_reverse)


class TestPeopleEdgeCases:
    @staticmethod
    def test_pagination_boundary_zero_page(api_client: APIClient) -> None:
        response = api_client.get("/api/people/?page=0")
        assert response.status_code == 404


class TestPeopleConsistency:
    @staticmethod
    def test_count_vs_list_consistency(api_client: APIClient, people_with_issues: list[Person]) -> None:
        assert api_client.get("/api/people/").data["count"] == api_client.get("/api/people/count/").data["count"]


class TestPeopleHTTPMethods:
    @staticmethod
    def test_list_endpoint_rejects_put(api_client: APIClient) -> None:
        response = api_client.put("/api/people/", {})
        assert response.status_code in [405, 403, 400]
