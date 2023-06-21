import pytest
from rest_framework.test import APIClient
from utils.utils import flatten_dict

from read_comics.users.models import User

from ..models import Issue

pytestmark = pytest.mark.django_db


class TestIssuesCount:
    @staticmethod
    def test_count(api_client: APIClient, issues: list[Issue]) -> None:
        response = api_client.get("/api/issues/count/")
        assert response.status_code == 200
        assert response.data["count"] == len(issues)


class TestIssuesList:
    list_keys = {
        "slug",
        "image",
        "start_year",
        "publisher__name",
        "publisher__image",
        "publisher__slug",
        "name",
        "short_description",
        "cover_date",
        "volume__slug",
        "volume__display_name",
        "volume__start_year",
        "volume__name",
        "finished_flg",
    }

    def test_dont_hide_finished(
        self, user: User, authenticated_api_client: APIClient, issues: list[Issue], finished_issues: list[Issue]
    ) -> None:
        response = authenticated_api_client.get("/api/issues/?hide-finished=no")

        assert response.status_code == 200
        assert response.data["count"] == len(issues) + len(finished_issues)

        flatten_response_data = [flatten_dict(response_item) for response_item in response.data["results"]]
        for item in flatten_response_data:
            assert self.list_keys == set(item.keys())

    def test_hide_finished(
        self, user: User, authenticated_api_client: APIClient, issues: list[Issue], finished_issues: list[Issue]
    ) -> None:
        response = authenticated_api_client.get("/api/issues/")

        assert response.status_code == 200
        assert response.data["count"] == len(issues)

        flatten_response_data = [flatten_dict(response_item) for response_item in response.data["results"]]
        for item in flatten_response_data:
            assert self.list_keys == set(item.keys())

    @staticmethod
    def test_finished_mark(user: User, authenticated_api_client: APIClient, finished_issue: Issue) -> None:
        response = authenticated_api_client.get("/api/issues/?hide-finished=no")
        response_data = response.data["results"][0]
        assert response_data["finished_flg"] == 1

    @staticmethod
    def test_no_finished_mark(user: User, authenticated_api_client: APIClient, issue: Issue) -> None:
        response = authenticated_api_client.get("/api/issues/")
        response_data = response.data["results"][0]
        assert response_data["finished_flg"] == 0

    @staticmethod
    def test_no_auth_finished_mark(api_client: APIClient, issue: Issue, finished_issue: Issue) -> None:
        response = api_client.get("/api/issues/")
        for response_issue in response.data["results"]:
            assert response_issue["finished_flg"] == 0

    @staticmethod
    def test_data(api_client: APIClient, issue: Issue) -> None:
        response = api_client.get("/api/issues/")

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
        assert response_data["volume"]["name"] == (issue.volume.name if issue.volume else None)
        assert response_data["volume"]["slug"] == (issue.volume.slug if issue.volume else None)
        assert response_data["volume"]["start_year"] == (issue.volume.start_year if issue.volume else None)


class TestIssueDetail:
    @staticmethod
    def test_data(api_client: APIClient, issue: Issue) -> None:
        response = api_client.get(f"/api/issues/{issue.slug}/")

        assert response.status_code == 200
        assert response.data["slug"] == issue.slug
        assert response.data["publisher"]["name"] == (
            issue.volume.publisher.name if issue.volume and issue.volume.publisher else None
        )
        assert response.data["publisher"]["slug"] == (
            issue.volume.publisher.slug if issue.volume and issue.volume.publisher else None
        )
        assert response.data["volume"]["display_name"] == (issue.volume.display_name if issue.volume else None)
        assert response.data["volume"]["name"] == (issue.volume.name if issue.volume else None)
        assert response.data["volume"]["slug"] == (issue.volume.slug if issue.volume else None)
        assert response.data["volume"]["start_year"] == (issue.volume.start_year if issue.volume else None)
        assert response.data["number"] == issue.number
        assert response.data["download_link"] == issue.download_link
        assert response.data["download_size"] == issue.download_size

    @staticmethod
    def test_anonymous_finished_flg_not_finished(api_client: APIClient, issue: Issue) -> None:
        response = api_client.get(f"/api/issues/{issue.slug}/")

        assert response.status_code == 200
        assert response.data["finished_flg"] == 0

    @staticmethod
    def test_anonymous_finished_flg_finished(api_client: APIClient, finished_issue: Issue) -> None:
        response = api_client.get(f"/api/issues/{finished_issue.slug}/")

        assert response.status_code == 200
        assert response.data["finished_flg"] == 0

    @staticmethod
    def test_finished_flg_not_finished(authenticated_api_client: APIClient, issue: Issue) -> None:
        response = authenticated_api_client.get(f"/api/issues/{issue.slug}/")

        assert response.status_code == 200
        assert response.data["finished_flg"] == 0

    @staticmethod
    def test_finished_flg_finished(authenticated_api_client: APIClient, finished_issue: Issue) -> None:
        response = authenticated_api_client.get(f"/api/issues/{finished_issue.slug}/")

        assert response.status_code == 200
        assert response.data["finished_flg"] == 1

    @staticmethod
    def test_prev_issue_slug_by_cover_date_asc(api_client: APIClient, issues: list[Issue]) -> None:
        ordered_issues = Issue.objects.order_by(
            "cover_date", "volume__name", "volume__start_year", "numerical_number", "number", "id"
        )
        first_issue = ordered_issues[0]
        second_issue = ordered_issues[1]

        response = api_client.get(
            f"/api/issues/{second_issue.slug}/"
            f"?ordering=cover_date,volume__name,volume__start_year,numerical_number,number"
        )

        assert response.data["prev_issue_slug"] == first_issue.slug

    @staticmethod
    def test_prev_issue_slug_by_cover_date_desc(api_client: APIClient, issues: list[Issue]) -> None:
        ordered_issues = Issue.objects.order_by(
            "-cover_date", "-volume__name", "-volume__start_year", "-numerical_number", "-number", "id"
        )
        first_issue = ordered_issues[0]
        second_issue = ordered_issues[1]

        response = api_client.get(
            f"/api/issues/{second_issue.slug}/"
            f"?ordering=-cover_date,-volume__name,-volume__start_year,-numerical_number,-number"
        )

        assert response.data["prev_issue_slug"] == first_issue.slug

    @staticmethod
    def test_prev_issue_slug_by_name_asc(api_client: APIClient, issues: list[Issue]) -> None:
        ordered_issues = Issue.objects.order_by(
            "volume__name", "volume__start_year", "numerical_number", "number", "id"
        )
        first_issue = ordered_issues[0]
        second_issue = ordered_issues[1]

        response = api_client.get(
            f"/api/issues/{second_issue.slug}/?ordering=volume__name,volume__start_year,numerical_number,number"
        )

        assert response.data["prev_issue_slug"] == first_issue.slug

    @staticmethod
    def test_prev_issue_slug_by_name_desc(api_client: APIClient, issues: list[Issue]) -> None:
        ordered_issues = Issue.objects.order_by(
            "-volume__name", "-volume__start_year", "-numerical_number", "-number", "-id"
        )
        first_issue = ordered_issues[0]
        second_issue = ordered_issues[1]

        response = api_client.get(
            f"/api/issues/{second_issue.slug}/?ordering=-volume__name,-volume__start_year,-numerical_number,-number"
        )

        assert response.data["prev_issue_slug"] == first_issue.slug

    @staticmethod
    def test_next_issue_slug_by_cover_date_asc(api_client: APIClient, issues: list[Issue]) -> None:
        ordered_issues = Issue.objects.order_by(
            "cover_date", "volume__name", "volume__start_year", "numerical_number", "number", "id"
        )
        first_issue = ordered_issues[0]
        second_issue = ordered_issues[1]

        response = api_client.get(
            f"/api/issues/{first_issue.slug}/"
            f"?ordering=cover_date,volume__name,volume__start_year,numerical_number,number"
        )

        assert response.data["next_issue_slug"] == second_issue.slug

    @staticmethod
    def test_next_issue_slug_by_cover_date_desc(api_client: APIClient, issues: list[Issue]) -> None:
        ordered_issues = Issue.objects.order_by(
            "-cover_date", "-volume__name", "-volume__start_year", "-numerical_number", "-number", "id"
        )
        first_issue = ordered_issues[0]
        second_issue = ordered_issues[1]

        response = api_client.get(
            f"/api/issues/{first_issue.slug}/"
            f"?ordering=-cover_date,-volume__name,-volume__start_year,-numerical_number,-number"
        )

        assert response.data["next_issue_slug"] == second_issue.slug

    @staticmethod
    def test_next_issue_slug_by_name_asc(api_client: APIClient, issues: list[Issue]) -> None:
        ordered_issues = Issue.objects.order_by(
            "volume__name", "volume__start_year", "numerical_number", "number", "id"
        )
        first_issue = ordered_issues[0]
        second_issue = ordered_issues[1]

        response = api_client.get(
            f"/api/issues/{first_issue.slug}/?ordering=volume__name,volume__start_year,numerical_number,number"
        )

        assert response.data["next_issue_slug"] == second_issue.slug

    @staticmethod
    def test_next_issue_slug_by_name_desc(api_client: APIClient, issues: list[Issue]) -> None:
        ordered_issues = Issue.objects.order_by(
            "-volume__name", "-volume__start_year", "-numerical_number", "-number", "-id"
        )
        first_issue = ordered_issues[0]
        second_issue = ordered_issues[1]

        response = api_client.get(
            f"/api/issues/{first_issue.slug}/?ordering=-volume__name,-volume__start_year,-numerical_number,-number"
        )

        assert response.data["next_issue_slug"] == second_issue.slug


class TestIssueTechnicalInfo:
    @staticmethod
    def test_no_auth(api_client: APIClient, issue: Issue) -> None:
        response = api_client.get(f"/api/issues/{issue.slug}/technical-info/")

        assert response.status_code == 401

    @staticmethod
    def test_regular_user(authenticated_api_client: APIClient, issue: Issue) -> None:
        response = authenticated_api_client.get(f"/api/issues/{issue.slug}/technical-info/")

        assert response.status_code == 403

    @staticmethod
    def test_staff(staff_api_client: APIClient, issue: Issue) -> None:
        response = staff_api_client.get(f"/api/issues/{issue.slug}/technical-info/")

        assert response.status_code == 200

    @staticmethod
    def test_superuser(superuser_api_client: APIClient, issue: Issue) -> None:
        response = superuser_api_client.get(f"/api/issues/{issue.slug}/technical-info/")

        assert response.status_code == 200

        assert response.data["id"] == issue.id
        assert response.data["comicvine_id"] == issue.comicvine_id
        assert response.data["comicvine_status"] == issue.get_comicvine_status_display()
        assert response.data["comicvine_last_match"] == issue.comicvine_last_match.strftime("%Y-%m-%dT%H:%M:%SZ")
        assert response.data["created_dt"] == issue.created_dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        assert response.data["modified_dt"] == issue.modified_dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
