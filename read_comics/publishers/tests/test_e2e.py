import pytest
from rest_framework.test import APIClient
from utils.utils import flatten_dict

from read_comics.issues.models import Issue

from ..models import Publisher

pytestmark = pytest.mark.django_db


class TestPublishersCount:
    # Count tests
    ##########################

    @staticmethod
    def test_count(
        api_client: APIClient, publishers_no_volumes: list[Publisher], publishers_with_volumes: list[Publisher]
    ) -> None:
        response = api_client.get("/api/publishers/count/")
        assert response.status_code == 200
        assert response.data["count"] == len(publishers_with_volumes)

    @staticmethod
    def test_count_all(
        api_client: APIClient, publishers_no_volumes: list[Publisher], publishers_with_volumes: list[Publisher]
    ) -> None:
        response = api_client.get("/api/publishers/count/?show-all=yes")
        assert response.status_code == 200
        assert response.data["count"] == len(publishers_with_volumes) + len(publishers_no_volumes)

    @staticmethod
    def test_empty_database(api_client: APIClient) -> None:
        response = api_client.get("/api/publishers/count/")
        assert response.status_code == 200
        assert response.data["count"] == 0


class TestPublishersList:
    list_keys = {"slug", "image", "name", "short_description", "issues_count", "volumes_count"}

    def test_no_show_all(
        self, api_client: APIClient, publishers_no_volumes: list[Publisher], publishers_with_volumes: list[Publisher]
    ) -> None:
        response = api_client.get("/api/publishers/")

        assert response.status_code == 200
        assert response.data["count"] == len(publishers_with_volumes)

        flatten_response_data = [flatten_dict(response_item) for response_item in response.data["results"]]
        for item in flatten_response_data:
            assert self.list_keys == set(item.keys())

    def test_show_all(
        self, api_client: APIClient, publishers_no_volumes: list[Publisher], publishers_with_volumes: list[Publisher]
    ) -> None:
        response = api_client.get("/api/publishers/?show-all=yes")

        assert response.status_code == 200
        assert response.data["count"] == len(publishers_no_volumes) + len(publishers_with_volumes)

        flatten_response_data = [flatten_dict(response_item) for response_item in response.data["results"]]
        for item in flatten_response_data:
            assert self.list_keys == set(item.keys())

    @staticmethod
    def test_data(api_client: APIClient, publisher_with_volumes: Publisher):
        response = api_client.get("/api/publishers/")

        assert response.status_code == 200
        assert response.data["count"] == 1

        response_data = response.data["results"][0]
        assert response_data["slug"] == publisher_with_volumes.slug
        assert response_data["name"] == publisher_with_volumes.name
        assert response_data["short_description"] == publisher_with_volumes.short_description
        assert (
            response_data["issues_count"]
            == Issue.objects.filter(volume__in=publisher_with_volumes.volumes.all()).count()
        )
        assert response_data["volumes_count"] == publisher_with_volumes.volumes.count()

    @staticmethod
    def test_empty_database(api_client: APIClient) -> None:
        response = api_client.get("/api/publishers/")
        assert response.status_code == 200
        assert response.data["count"] == 0
        assert response.data["results"] == []

    @staticmethod
    def test_default_ordering_by_name(api_client: APIClient, publishers_with_volumes: list[Publisher]) -> None:
        response = api_client.get("/api/publishers/")

        assert response.status_code == 200
        assert response.data["count"] == len(publishers_with_volumes)

        names = [item["name"] for item in response.data["results"]]
        assert names == sorted(names)

    @staticmethod
    def test_ordering_by_name_ascending(api_client: APIClient, publishers_with_volumes: list[Publisher]) -> None:
        response = api_client.get("/api/publishers/?ordering=name")

        assert response.status_code == 200
        names = [item["name"] for item in response.data["results"]]
        assert names == sorted(names)

    @staticmethod
    def test_ordering_by_name_descending(api_client: APIClient, publishers_with_volumes: list[Publisher]) -> None:
        response = api_client.get("/api/publishers/?ordering=-name")

        assert response.status_code == 200
        names = [item["name"] for item in response.data["results"]]
        assert names == sorted(names, reverse=True)

    @staticmethod
    def test_ordering_by_issues_count_ascending(
        api_client: APIClient, publishers_with_volumes: list[Publisher]
    ) -> None:
        response = api_client.get("/api/publishers/?ordering=issues_count")

        assert response.status_code == 200
        issues_counts = [item["issues_count"] for item in response.data["results"]]
        assert issues_counts == sorted(issues_counts)

    @staticmethod
    def test_ordering_by_issues_count_descending(
        api_client: APIClient, publishers_with_volumes: list[Publisher]
    ) -> None:
        response = api_client.get("/api/publishers/?ordering=-issues_count")

        assert response.status_code == 200
        issues_counts = [item["issues_count"] for item in response.data["results"]]
        assert issues_counts == sorted(issues_counts, reverse=True)

    @staticmethod
    def test_ordering_by_volumes_count_ascending(
        api_client: APIClient, publishers_with_volumes: list[Publisher]
    ) -> None:
        response = api_client.get("/api/publishers/?ordering=volumes_count")

        assert response.status_code == 200
        volumes_counts = [item["volumes_count"] for item in response.data["results"]]
        assert volumes_counts == sorted(volumes_counts)

    @staticmethod
    def test_ordering_by_volumes_count_descending(
        api_client: APIClient, publishers_with_volumes: list[Publisher]
    ) -> None:
        response = api_client.get("/api/publishers/?ordering=-volumes_count")

        assert response.status_code == 200
        volumes_counts = [item["volumes_count"] for item in response.data["results"]]
        assert volumes_counts == sorted(volumes_counts, reverse=True)

    @staticmethod
    def test_invalid_ordering_field(api_client: APIClient, publishers_with_volumes: list[Publisher]) -> None:
        response = api_client.get("/api/publishers/?ordering=invalid_field")

        assert response.status_code == 200
        names = [item["name"] for item in response.data["results"]]
        assert names == sorted(names)

    @staticmethod
    def test_pagination_invalid_page(api_client: APIClient, publishers_with_volumes: list[Publisher]) -> None:
        response = api_client.get("/api/publishers/?page=999")

        assert response.status_code == 404


class TestPublishersParametrized:
    @pytest.mark.parametrize("ordering,is_reverse", [("name", False), ("-name", True)])
    def test_ordering_parametrized(self, api_client: APIClient, publishers_with_volumes: list[Publisher], ordering: str, is_reverse: bool) -> None:
        response = api_client.get(f"/api/publishers/?ordering={ordering}")
        assert response.status_code == 200
        values = [item[ordering.lstrip("-")] for item in response.data["results"]]
        assert values == sorted(values, reverse=is_reverse)


class TestPublishersEdgeCases:
    @staticmethod
    def test_pagination_boundary_negative_page(api_client: APIClient) -> None:
        response = api_client.get("/api/publishers/?page=-1")
        assert response.status_code == 404


class TestPublishersConsistency:
    @staticmethod
    def test_count_vs_list_consistency(api_client: APIClient, publishers_with_volumes: list[Publisher]) -> None:
        assert api_client.get("/api/publishers/").data["count"] == api_client.get("/api/publishers/count/").data["count"]


class TestPublishersHTTPMethods:
    @staticmethod
    def test_detail_endpoint_rejects_delete(api_client: APIClient, publisher_with_volumes: Publisher) -> None:
        response = api_client.delete(f"/api/publishers/{publisher_with_volumes.slug}/")
        assert response.status_code in [405, 403, 400]
