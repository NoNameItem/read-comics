from django.urls import resolve, reverse


class TestPublishersApiUrls:
    @staticmethod
    def test_count() -> None:
        assert reverse("api:publisher-count") == "/api/publishers/count/"
        assert resolve("/api/publishers/count/").view_name == "api:publisher-count"
