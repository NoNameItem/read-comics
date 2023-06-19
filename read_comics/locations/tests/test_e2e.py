import pytest
from django.db.models import Count
from rest_framework.test import APIClient
from utils.utils import flatten_dict

from ..models import Location

pytestmark = pytest.mark.django_db


class TestLocationsE2E:
    # Count tests
    ##########################

    @staticmethod
    def test_count(
        api_client: APIClient, locations_no_issues: list[Location], locations_with_issues: list[Location]
    ) -> None:
        response = api_client.get("/api/locations/count/")
        assert response.status_code == 200
        assert response.data["count"] == len(locations_with_issues)

    @staticmethod
    def test_count_all(
        api_client: APIClient, locations_no_issues: list[Location], locations_with_issues: list[Location]
    ) -> None:
        response = api_client.get("/api/locations/count/?show-all=yes")
        assert response.status_code == 200
        assert response.data["count"] == len(locations_with_issues) + len(locations_no_issues)


class TestLocationsList:
    list_keys = {"slug", "image", "name", "short_description", "issues_count", "volumes_count"}

    def test_no_show_all(
        self, api_client: APIClient, locations_no_issues: list[Location], locations_with_issues: list[Location]
    ) -> None:
        response = api_client.get("/api/locations/")

        assert response.status_code == 200
        assert response.data["count"] == len(locations_with_issues)

        flatten_response_data = [flatten_dict(response_item) for response_item in response.data["results"]]
        for item in flatten_response_data:
            assert self.list_keys == set(item.keys())

    def test_show_all(
        self, api_client: APIClient, locations_no_issues: list[Location], locations_with_issues: list[Location]
    ) -> None:
        response = api_client.get("/api/locations/?show-all=yes")

        assert response.status_code == 200
        assert response.data["count"] == len(locations_no_issues) + len(locations_with_issues)

        flatten_response_data = [flatten_dict(response_item) for response_item in response.data["results"]]
        for item in flatten_response_data:
            assert self.list_keys == set(item.keys())

    @staticmethod
    def test_data(api_client: APIClient, location_with_issues: Location):
        response = api_client.get("/api/locations/")

        assert response.status_code == 200
        assert response.data["count"] == 1

        response_data = response.data["results"][0]
        assert response_data["slug"] == location_with_issues.slug
        assert response_data["name"] == location_with_issues.name
        assert response_data["short_description"] == location_with_issues.short_description
        assert response_data["issues_count"] == location_with_issues.issues.count()
        assert (
            response_data["volumes_count"]
            == location_with_issues.issues.aggregate(v=Count("volume", distinct=True))["v"]
        )
