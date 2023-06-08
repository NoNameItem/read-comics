from django.urls import resolve, reverse


class TestTeamsApiUrls:
    @staticmethod
    def test_count() -> None:
        assert reverse("api:team-count") == "/api/teams/count/"
        assert resolve("/api/teams/count/").view_name == "api:team-count"
