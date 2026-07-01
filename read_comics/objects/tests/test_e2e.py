# Docs: [[docs/backend/objects/testing/test_e2e.md]]
import pytest
from django.db.models import Count
from rest_framework.test import APIClient
from utils.utils import flatten_dict

from ..models import Object

pytestmark = pytest.mark.django_db


class TestObjectsCount:
    # Count tests
    ##########################

    @staticmethod
    def test_count(api_client: APIClient, objects_no_issues: list[Object], objects_with_issues: list[Object]) -> None:
        response = api_client.get("/api/objects/count/")
        assert response.status_code == 200
        assert response.data["count"] == len(objects_with_issues)

    @staticmethod
    def test_count_all(
        api_client: APIClient, objects_no_issues: list[Object], objects_with_issues: list[Object]
    ) -> None:
        response = api_client.get("/api/objects/count/?show-all=yes")
        assert response.status_code == 200
        assert response.data["count"] == len(objects_with_issues) + len(objects_no_issues)

    @staticmethod
    def test_empty_database(api_client: APIClient) -> None:
        response = api_client.get("/api/objects/count/")
        assert response.status_code == 200
        assert response.data["count"] == 0


class TestObjectsList:
    list_keys = {"slug", "image", "name", "short_description", "issues_count", "volumes_count"}

    def test_no_show_all(
        self, api_client: APIClient, objects_no_issues: list[Object], objects_with_issues: list[Object]
    ) -> None:
        response = api_client.get("/api/objects/")

        assert response.status_code == 200
        assert response.data["count"] == len(objects_with_issues)

        flatten_response_data = [flatten_dict(response_item) for response_item in response.data["results"]]
        for item in flatten_response_data:
            assert self.list_keys == set(item.keys())

    def test_show_all(
        self, api_client: APIClient, objects_no_issues: list[Object], objects_with_issues: list[Object]
    ) -> None:
        response = api_client.get("/api/objects/?show-all=yes")

        assert response.status_code == 200
        assert response.data["count"] == len(objects_no_issues) + len(objects_with_issues)

        flatten_response_data = [flatten_dict(response_item) for response_item in response.data["results"]]
        for item in flatten_response_data:
            assert self.list_keys == set(item.keys())

    @staticmethod
    def test_data(api_client: APIClient, object_with_issues: Object):
        response = api_client.get("/api/objects/")

        assert response.status_code == 200
        assert response.data["count"] == 1

        response_data = response.data["results"][0]
        assert response_data["slug"] == object_with_issues.slug
        assert response_data["name"] == object_with_issues.name
        assert response_data["short_description"] == object_with_issues.short_description
        assert response_data["issues_count"] == object_with_issues.issues.count()
        assert (
            response_data["volumes_count"] == object_with_issues.issues.aggregate(v=Count("volume", distinct=True))["v"]
        )

    @staticmethod
    def test_empty_database(api_client: APIClient) -> None:
        response = api_client.get("/api/objects/")
        assert response.status_code == 200
        assert response.data["count"] == 0
        assert response.data["results"] == []

    @staticmethod
    def test_default_ordering_by_name(api_client: APIClient, objects_with_issues: list[Object]) -> None:
        response = api_client.get("/api/objects/")

        assert response.status_code == 200
        assert response.data["count"] == len(objects_with_issues)

        names = [item["name"] for item in response.data["results"]]
        assert names == sorted(names)

    @staticmethod
    def test_ordering_by_name_ascending(api_client: APIClient, objects_with_issues: list[Object]) -> None:
        response = api_client.get("/api/objects/?ordering=name")

        assert response.status_code == 200
        names = [item["name"] for item in response.data["results"]]
        assert names == sorted(names)

    @staticmethod
    def test_ordering_by_name_descending(api_client: APIClient, objects_with_issues: list[Object]) -> None:
        response = api_client.get("/api/objects/?ordering=-name")

        assert response.status_code == 200
        names = [item["name"] for item in response.data["results"]]
        assert names == sorted(names, reverse=True)

    @staticmethod
    def test_ordering_by_issues_count_ascending(api_client: APIClient, objects_with_issues: list[Object]) -> None:
        response = api_client.get("/api/objects/?ordering=issues_count")

        assert response.status_code == 200
        issues_counts = [item["issues_count"] for item in response.data["results"]]
        assert issues_counts == sorted(issues_counts)

    @staticmethod
    def test_ordering_by_issues_count_descending(api_client: APIClient, objects_with_issues: list[Object]) -> None:
        response = api_client.get("/api/objects/?ordering=-issues_count")

        assert response.status_code == 200
        issues_counts = [item["issues_count"] for item in response.data["results"]]
        assert issues_counts == sorted(issues_counts, reverse=True)

    @staticmethod
    def test_ordering_by_volumes_count_ascending(api_client: APIClient, objects_with_issues: list[Object]) -> None:
        response = api_client.get("/api/objects/?ordering=volumes_count")

        assert response.status_code == 200
        volumes_counts = [item["volumes_count"] for item in response.data["results"]]
        assert volumes_counts == sorted(volumes_counts)

    @staticmethod
    def test_ordering_by_volumes_count_descending(api_client: APIClient, objects_with_issues: list[Object]) -> None:
        response = api_client.get("/api/objects/?ordering=-volumes_count")

        assert response.status_code == 200
        volumes_counts = [item["volumes_count"] for item in response.data["results"]]
        assert volumes_counts == sorted(volumes_counts, reverse=True)

    @staticmethod
    def test_invalid_ordering_field(api_client: APIClient, objects_with_issues: list[Object]) -> None:
        """Test that invalid ordering field falls back to default ordering."""
        default_response = api_client.get("/api/objects/")
        invalid_ordering_response = api_client.get("/api/objects/?ordering=invalid_field")

        assert invalid_ordering_response.status_code == 200

        default_names = [item["name"] for item in default_response.data["results"]]
        invalid_ordering_names = [item["name"] for item in invalid_ordering_response.data["results"]]
        assert invalid_ordering_names == default_names

    @staticmethod
    def test_pagination_invalid_page(api_client: APIClient, objects_with_issues: list[Object]) -> None:
        response = api_client.get("/api/objects/?page=999")

        assert response.status_code == 404


class TestObjectsParametrized:
    @pytest.mark.parametrize("ordering,is_reverse", [("name", False), ("-name", True)])
    def test_ordering_parametrized(
        self, api_client: APIClient, objects_with_issues: list[Object], ordering: str, is_reverse: bool
    ) -> None:
        response = api_client.get(f"/api/objects/?ordering={ordering}")
        assert response.status_code == 200
        field = ordering.lstrip("-")
        values = [item[field] for item in response.data["results"]]
        assert values == sorted(values, reverse=is_reverse)


class TestObjectsEdgeCases:
    @staticmethod
    def test_pagination_boundary_first_page(api_client: APIClient, objects_with_issues: list[Object]) -> None:
        response = api_client.get("/api/objects/?page=1")
        assert response.status_code == 200


class TestObjectsConsistency:
    @staticmethod
    def test_count_vs_list_count_consistency(api_client: APIClient, objects_with_issues: list[Object]) -> None:
        list_response = api_client.get("/api/objects/")
        count_response = api_client.get("/api/objects/count/")
        assert list_response.data["count"] == count_response.data["count"]


class TestObjectsHTTPMethods:
    @staticmethod
    def test_list_endpoint_rejects_post(api_client: APIClient) -> None:
        response = api_client.post("/api/objects/", {"name": "New"})
        assert response.status_code in [405, 403, 400]
