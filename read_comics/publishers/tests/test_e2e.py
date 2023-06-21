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
