from django.urls import resolve, reverse


class TestMissingIssuesApiUrls:
    @staticmethod
    def test_count() -> None:
        assert reverse("api:missing-issue-count") == "/api/missing-issues/count/"
        assert resolve("/api/missing-issues/count/").view_name == "api:missing-issue-count"
