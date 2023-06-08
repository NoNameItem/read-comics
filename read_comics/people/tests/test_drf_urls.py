from django.urls import resolve, reverse


class TestPeopleApiUrls:
    @staticmethod
    def test_count() -> None:
        assert reverse("api:people-count") == "/api/people/count/"
        assert resolve("/api/people/count/").view_name == "api:people-count"
