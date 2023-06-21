from django.urls import resolve, reverse


class TestVolumesApiUrls:
    @staticmethod
    def test_count() -> None:
        assert reverse("api:volume-count") == "/api/volumes/count/"
        assert resolve("/api/volumes/count/").view_name == "api:volume-count"

    @staticmethod
    def test_list() -> None:
        assert reverse("api:volume-list") == "/api/volumes/"
        assert resolve("/api/volumes/").view_name == "api:volume-list"

    @staticmethod
    def test_started() -> None:
        assert reverse("api:volume-started") == "/api/volumes/started/"
        assert resolve("/api/volumes/started/").view_name == "api:volume-started"
