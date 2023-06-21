from django.urls import resolve, reverse


class TestObjectsApiUrls:
    @staticmethod
    def test_count() -> None:
        assert reverse("api:object-count") == "/api/objects/count/"
        assert resolve("/api/objects/count/").view_name == "api:object-count"

    @staticmethod
    def test_list() -> None:
        assert reverse("api:object-list") == "/api/objects/"
        assert resolve("/api/objects/").view_name == "api:object-list"
