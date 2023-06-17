import pytest
from utils.utils import flatten_dict

from ..models import Issue

pytestmark = pytest.mark.django_db


class TestIssuesCount:
    @staticmethod
    def test_count(api_client, issues) -> None:
        response = api_client().get("/api/issues/count/")
        assert response.status_code == 200
        assert response.data["count"] == len(issues)


class TestIssuesList:
    list_keys = {
        "slug",
        "image",
        "publisher__name",
        "publisher__image",
        "publisher__slug",
        "name",
        "short_description",
        "cover_date",
        "volume__slug",
        "volume__display_name",
        "volume__start_year",
        "finished_flg",
    }

    def test_dont_hide_finished(
        self, user, authenticated_api_client, issues: list[Issue], finished_issues: list[Issue]
    ) -> None:
        response = authenticated_api_client.get("/api/issues/?hide-finished=no")

        assert response.status_code == 200
        assert response.data["count"] == len(issues) + len(finished_issues)

        flatten_response_data = [flatten_dict(response_item) for response_item in response.data["results"]]
        for item in flatten_response_data:
            assert self.list_keys == set(item.keys())

    def test_hide_finished(
        self, user, authenticated_api_client, issues: list[Issue], finished_issues: list[Issue]
    ) -> None:
        response = authenticated_api_client.get("/api/issues/")

        assert response.status_code == 200
        assert response.data["count"] == len(issues)

        flatten_response_data = [flatten_dict(response_item) for response_item in response.data["results"]]
        for item in flatten_response_data:
            assert self.list_keys == set(item.keys())

    @staticmethod
    def test_finished_mark(user, authenticated_api_client, finished_issue: Issue):
        response = authenticated_api_client.get("/api/issues/?hide-finished=no")
        response_data = response.data["results"][0]
        assert response_data["finished_flg"] == 1

    @staticmethod
    def test_no_finished_mark(user, authenticated_api_client, issue: Issue):
        response = authenticated_api_client.get("/api/issues/")
        response_data = response.data["results"][0]
        assert response_data["finished_flg"] == 0

    @staticmethod
    def test_no_auth_finished_mark(api_client, issue: Issue, finished_issue):
        response = api_client().get("/api/issues/")
        for response_issue in response.data["results"]:
            assert response_issue["finished_flg"] == 0

    @staticmethod
    def test_data(api_client, issue: Issue):
        response = api_client().get("/api/issues/")

        response_data = response.data["results"][0]
        assert response_data["slug"] == issue.slug
        assert response_data["name"] == issue.display_name
        assert response_data["publisher"]["name"] == (
            issue.volume.publisher.name if issue.volume and issue.volume.publisher else None
        )
        assert response_data["publisher"]["slug"] == (
            issue.volume.publisher.slug if issue.volume and issue.volume.publisher else None
        )
        assert response_data["short_description"] == issue.short_description
        assert response_data["cover_date"] == issue.cover_date.isoformat()
        assert response_data["volume"]["display_name"] == (issue.volume.display_name if issue.volume else None)
        assert response_data["volume"]["slug"] == (issue.volume.slug if issue.volume else None)
        assert response_data["volume"]["start_year"] == (issue.volume.start_year if issue.volume else None)
