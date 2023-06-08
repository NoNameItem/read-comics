from django.urls import resolve, reverse


class TestLocationsApiUrls:
    @staticmethod
    def test_count() -> None:
        assert reverse("api:location-count") == "/api/locations/count/"
        assert resolve("/api/locations/count/").view_name == "api:location-count"
