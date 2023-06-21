import pytest
from django.urls import resolve, reverse


class TestIssuesApiUrls:
    base_url = "issues"
    base_name = "issue"

    @staticmethod
    def test_count() -> None:
        assert reverse("api:issue-count") == "/api/issues/count/"
        assert resolve("/api/issues/count/").view_name == "api:issue-count"

    @staticmethod
    def test_list() -> None:
        assert reverse("api:issue-list") == "/api/issues/"
        assert resolve("/api/issues/").view_name == "api:issue-list"

    @staticmethod
    @pytest.mark.django_db
    def test_detail(issue) -> None:
        assert reverse("api:issue-detail", kwargs={"slug": issue.slug}) == f"/api/issues/{issue.slug}/"
        assert resolve(f"/api/issues/{issue.slug}/").view_name == "api:issue-detail"

    @staticmethod
    @pytest.mark.django_db
    def test_technical_info(issue) -> None:
        assert (
            reverse("api:issue-technical-info", kwargs={"slug": issue.slug})
            == f"/api/issues/{issue.slug}/technical-info/"
        )
        assert resolve(f"/api/issues/{issue.slug}/technical-info/").view_name == "api:issue-technical-info"
