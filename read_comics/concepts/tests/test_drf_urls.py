from django.urls import resolve, reverse


class TestConceptsApiUrls:
    @staticmethod
    def test_count() -> None:
        assert reverse("api:concept-count") == "/api/concepts/count/"
        assert resolve("/api/concepts/count/").view_name == "api:concept-count"
