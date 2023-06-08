from django.urls import resolve, reverse


class TestIssuesApiUrls:
    base_url = "issues"
    base_name = "issue"

    @staticmethod
    def test_count() -> None:
        assert reverse("api:issue-count") == "/api/issues/count/"
        assert resolve("/api/issues/count/").view_name == "api:issue-count"
