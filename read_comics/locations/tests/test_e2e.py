import sys

import pytest
from django.db.models import Count
from django.utils import timezone
from rest_framework.test import APIClient
from utils.utils import flatten_dict

from ..models import Location

pytestmark = pytest.mark.django_db


class TestLocationsCount:
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

    @staticmethod
    def test_default_ordering_by_name(api_client: APIClient, locations_with_issues: list[Location]) -> None:
        response = api_client.get("/api/locations/")

        assert response.status_code == 200
        assert response.data["count"] == len(locations_with_issues)

        names = [item["name"] for item in response.data["results"]]
        assert names == sorted(names)

    @staticmethod
    def test_ordering_by_name_ascending(api_client: APIClient, locations_with_issues: list[Location]) -> None:
        response = api_client.get("/api/locations/?ordering=name")

        assert response.status_code == 200
        names = [item["name"] for item in response.data["results"]]
        assert names == sorted(names)

    @staticmethod
    def test_ordering_by_name_descending(api_client: APIClient, locations_with_issues: list[Location]) -> None:
        response = api_client.get("/api/locations/?ordering=-name")

        assert response.status_code == 200
        names = [item["name"] for item in response.data["results"]]
        assert names == sorted(names, reverse=True)

    @staticmethod
    def test_ordering_by_issues_count_ascending(api_client: APIClient, locations_with_issues: list[Location]) -> None:
        response = api_client.get("/api/locations/?ordering=issues_count")

        assert response.status_code == 200
        issues_counts = [item["issues_count"] for item in response.data["results"]]
        assert issues_counts == sorted(issues_counts)

    @staticmethod
    def test_ordering_by_issues_count_descending(api_client: APIClient, locations_with_issues: list[Location]) -> None:
        response = api_client.get("/api/locations/?ordering=-issues_count")

        assert response.status_code == 200
        issues_counts = [item["issues_count"] for item in response.data["results"]]
        assert issues_counts == sorted(issues_counts, reverse=True)

    @staticmethod
    def test_ordering_by_volumes_count_ascending(api_client: APIClient, locations_with_issues: list[Location]) -> None:
        response = api_client.get("/api/locations/?ordering=volumes_count")

        assert response.status_code == 200
        volumes_counts = [item["volumes_count"] for item in response.data["results"]]
        assert volumes_counts == sorted(volumes_counts)

    @staticmethod
    def test_ordering_by_volumes_count_descending(api_client: APIClient, locations_with_issues: list[Location]) -> None:
        response = api_client.get("/api/locations/?ordering=-volumes_count")

        assert response.status_code == 200
        volumes_counts = [item["volumes_count"] for item in response.data["results"]]
        assert volumes_counts == sorted(volumes_counts, reverse=True)

    @staticmethod
    def test_invalid_ordering_field(api_client: APIClient, locations_with_issues: list[Location]) -> None:
        response = api_client.get("/api/locations/?ordering=invalid_field")

        assert response.status_code == 200
        names = [item["name"] for item in response.data["results"]]
        assert names == sorted(names)

    @staticmethod
    def test_pagination_invalid_page(api_client: APIClient, locations_with_issues: list[Location]) -> None:
        response = api_client.get("/api/locations/?page=999")

        assert response.status_code == 404


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

    @staticmethod
    def test_not_found(api_client: APIClient) -> None:
        response = api_client.get("/api/locations/does-not-exist/")

        assert response.status_code == 404


class TestLocationTechnicalInfo:
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
    @pytest.mark.skipif(sys.version_info < (3, 12), reason="requires Python 3.12 or later")
    def test_superuser(superuser_api_client: APIClient, location_with_issues: Location) -> None:
        response = superuser_api_client.get(f"/api/locations/{location_with_issues.slug}/technical-info/")

        assert response.status_code == 200

        assert response.data["id"] == location_with_issues.id
        assert response.data["comicvine_id"] == location_with_issues.comicvine_id
        assert response.data["comicvine_status"] == location_with_issues.get_comicvine_status_display()
        assert (
            response.data["comicvine_last_match"]
            == timezone.localtime(location_with_issues.comicvine_last_match).isoformat()
        )
        assert response.data["created_dt"] == timezone.localtime(location_with_issues.created_dt).isoformat()
        assert response.data["modified_dt"] == timezone.localtime(location_with_issues.modified_dt).isoformat()


class TestLocationsParametrized:
    @pytest.mark.parametrize("ordering,is_reverse", [("name", False), ("-name", True), ("issues_count", False), ("-issues_count", True)])
    def test_ordering_parametrized(self, api_client: APIClient, locations_with_issues: list[Location], ordering: str, is_reverse: bool) -> None:
        response = api_client.get(f"/api/locations/?ordering={ordering}")
        assert response.status_code == 200
        field = ordering.lstrip("-")
        values = [item[field] for item in response.data["results"]]
        assert values == sorted(values, reverse=is_reverse)


class TestLocationsEdgeCases:
    @staticmethod
    def test_pagination_boundary_first_page(api_client: APIClient, locations_with_issues: list[Location]) -> None:
        response = api_client.get("/api/locations/?page=1")
        assert response.status_code == 200
        assert "results" in response.data

    @staticmethod
    def test_pagination_boundary_zero_page(api_client: APIClient) -> None:
        response = api_client.get("/api/locations/?page=0")
        assert response.status_code == 404


class TestLocationsConsistency:
    @staticmethod
    def test_count_vs_list_count_consistency(api_client: APIClient, locations_with_issues: list[Location]) -> None:
        list_response = api_client.get("/api/locations/")
        count_response = api_client.get("/api/locations/count/")
        assert list_response.data["count"] == count_response.data["count"]


class TestLocationsHTTPMethods:
    @staticmethod
    def test_list_endpoint_rejects_post(api_client: APIClient) -> None:
        response = api_client.post("/api/locations/", {"name": "New"})
        assert response.status_code in [405, 403, 400]

    @staticmethod
    def test_response_content_type_is_json(api_client: APIClient) -> None:
        response = api_client.get("/api/locations/")
        assert "application/json" in response.get("Content-Type", "")
