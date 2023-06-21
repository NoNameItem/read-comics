import pytest
from django.urls import resolve, reverse


class TestLocationsApiUrls:
    @staticmethod
    def test_count() -> None:
        assert reverse("api:location-count") == "/api/locations/count/"
        assert resolve("/api/locations/count/").view_name == "api:location-count"

    @staticmethod
    def test_list() -> None:
        assert reverse("api:location-list") == "/api/locations/"
        assert resolve("/api/locations/").view_name == "api:location-list"

    @staticmethod
    @pytest.mark.django_db
    def test_detail(location_with_issues) -> None:
        assert (
            reverse("api:location-detail", kwargs={"slug": location_with_issues.slug})
            == f"/api/locations/{location_with_issues.slug}/"
        )
        assert resolve(f"/api/locations/{location_with_issues.slug}/").view_name == "api:location-detail"

    @staticmethod
    @pytest.mark.django_db
    def test_technical_info(location_with_issues) -> None:
        assert (
            reverse("api:location-technical-info", kwargs={"slug": location_with_issues.slug})
            == f"/api/locations/{location_with_issues.slug}/technical-info/"
        )
        assert (
            resolve(f"/api/locations/{location_with_issues.slug}/technical-info/").view_name
            == "api:location-technical-info"
        )
