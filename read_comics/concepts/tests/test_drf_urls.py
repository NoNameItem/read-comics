from django.urls import resolve, reverse


class TestConceptsApiUrls:
    @staticmethod
    def test_count() -> None:
        assert reverse("api:concept-count") == "/api/concepts/count/"
        assert resolve("/api/concepts/count/").view_name == "api:concept-count"

    @staticmethod
    def test_list() -> None:
        assert reverse("api:concept-list") == "/api/concepts/"
        assert resolve("/api/concepts/").view_name == "api:concept-list"
