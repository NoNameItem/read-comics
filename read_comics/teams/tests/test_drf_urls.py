from django.urls import resolve, reverse


class TestTeamsApiUrls:
    @staticmethod
    def test_count() -> None:
        assert reverse("api:team-count") == "/api/teams/count/"
        assert resolve("/api/teams/count/").view_name == "api:team-count"

    @staticmethod
    def test_list() -> None:
        assert reverse("api:team-list") == "/api/teams/"
        assert resolve("/api/teams/").view_name == "api:team-list"
