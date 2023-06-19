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


class TestLocationDetail:
    @staticmethod
    def test_with_first_issue(api_client: APIClient, location_with_issues: Location) -> None:
        response = api_client.get(f"/api/locations/{location_with_issues.slug}/")

        assert response.status_code == 200

        assert response.data["slug"] == location_with_issues.slug
        assert response.data["name"] == location_with_issues.name
        assert response.data["aliases"] == location_with_issues.get_aliases_list()
        assert response.data["start_year"] == location_with_issues.start_year
        assert response.data["first_issue_name"] == (
            location_with_issues.first_issue.display_name if location_with_issues.first_issue is not None else None
        )
        assert response.data["first_issue_slug"] == (
            location_with_issues.first_issue.slug if location_with_issues.first_issue is not None else None
        )
        assert response.data["comicvine_url"] == location_with_issues.comicvine_url
        assert response.data["short_description"] == location_with_issues.short_description
        assert response.data["description"] == location_with_issues.description
        assert response.data["download_size"] == location_with_issues.download_size
        assert response.data["download_link"] == f"http://testserver{location_with_issues.download_link}"

    @staticmethod
    def test_no_first_issue(api_client: APIClient, location_no_issues: Location) -> None:
        response = api_client.get(f"/api/locations/{location_no_issues.slug}/")

        assert response.status_code == 200

        assert response.data["first_issue_name"] == location_no_issues.first_issue_name
        assert response.data["first_issue_slug"] is None
        assert response.data["download_size"] == "0\xa0bytes"


class TestConceptTechnicalInfo:
    @staticmethod
    def test_no_auth(api_client: APIClient, location_with_issues: Location) -> None:
        response = api_client.get(f"/api/locations/{location_with_issues.slug}/technical-info/")

        assert response.status_code == 401

    @staticmethod
    def test_regular_user(authenticated_api_client: APIClient, location_with_issues: Location) -> None:
        response = authenticated_api_client.get(f"/api/locations/{location_with_issues.slug}/technical-info/")

        assert response.status_code == 403

    @staticmethod
    def test_staff(staff_api_client: APIClient, location_with_issues: Location) -> None:
        response = staff_api_client.get(f"/api/locations/{location_with_issues.slug}/technical-info/")

        assert response.status_code == 200

    @staticmethod
    def test_superuser(superuser_api_client: APIClient, location_with_issues: Location) -> None:
        response = superuser_api_client.get(f"/api/locations/{location_with_issues.slug}/technical-info/")

        assert response.status_code == 200

        assert response.data["id"] == location_with_issues.id
        assert response.data["comicvine_id"] == location_with_issues.comicvine_id
        assert response.data["comicvine_status"] == location_with_issues.get_comicvine_status_display()
        assert response.data["comicvine_last_match"] == location_with_issues.comicvine_last_match.strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
        assert response.data["created_dt"] == location_with_issues.created_dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        assert response.data["modified_dt"] == location_with_issues.modified_dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
