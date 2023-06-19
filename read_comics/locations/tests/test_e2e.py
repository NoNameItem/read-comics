import pytest
from rest_framework.test import APIClient

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
