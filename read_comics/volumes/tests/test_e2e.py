from datetime import datetime, timedelta
from random import randrange

import pytest
from django.db.models import Max
from django.utils.dateparse import parse_datetime
from rest_framework.test import APIClient

from read_comics.issues.models import FinishedIssue
from read_comics.issues.tests.factories import FinishedIssueFactory, IssueFactory
from read_comics.users.models import User
from read_comics.utils.utils import flatten_dict

from ..models import Volume
from .factories import VolumeFactory

pytestmark = pytest.mark.django_db


class TestVolumesCount:
    @staticmethod
    def test_count(
        user: User,
        authenticated_api_client: APIClient,
        volumes_no_issues: list[Volume],
        volumes_with_issues: list[Volume],
        finished_volumes: list[Volume],
    ) -> None:
        response = authenticated_api_client.get("/api/volumes/count/")
        assert response.status_code == 200
        assert response.data["count"] == len(volumes_with_issues) + len(volumes_no_issues) + len(finished_volumes)


class TestVolumesList:
    list_keys = {
        "slug",
        "image",
        "start_year",
        "publisher__name",
        "publisher__image",
        "publisher__slug",
        "name",
        "short_description",
        "issues_count",
        "finished_count",
        "is_finished",
    }

    def test_dont_hide_finished(
        self,
        user: User,
        authenticated_api_client: APIClient,
        volumes_with_issues: list[Volume],
        finished_volumes: list[Volume],
    ) -> None:
        response = authenticated_api_client.get("/api/volumes/?hide-finished=no")

        assert response.status_code == 200
        assert response.data["count"] == len(volumes_with_issues) + len(finished_volumes)

        flatten_response_data = [flatten_dict(response_item) for response_item in response.data["results"]]
        for item in flatten_response_data:
            assert self.list_keys == set(item.keys())

    def test_hide_finished(
        self,
        user: User,
        authenticated_api_client: APIClient,
        volumes_with_issues: list[Volume],
        finished_volumes: list[Volume],
    ) -> None:
        response = authenticated_api_client.get("/api/volumes/")

        assert response.status_code == 200
        assert response.data["count"] == len(volumes_with_issues)

        flatten_response_data = [flatten_dict(response_item) for response_item in response.data["results"]]
        for item in flatten_response_data:
            assert self.list_keys == set(item.keys())

    @staticmethod
    def test_finished_mark(user: User, authenticated_api_client: APIClient, finished_volume: Volume) -> None:
        response = authenticated_api_client.get("/api/volumes/?hide-finished=no")
        response_data = response.data["results"][0]
        assert response_data["is_finished"]

    @staticmethod
    def test_no_finished_mark(user: User, authenticated_api_client: APIClient, volume_with_issues: Volume) -> None:
        response = authenticated_api_client.get("/api/volumes/")
        response_data = response.data["results"][0]
        assert not response_data["is_finished"]

    @staticmethod
    def test_no_auth_finished_mark(api_client: APIClient, volume_with_issues: Volume, finished_volume: Volume) -> None:
        response = api_client.get("/api/volumes/")
        for response_issue in response.data["results"]:
            assert response_issue["is_finished"] is None

    @staticmethod
    def test_data(api_client: APIClient, volume_with_issues: Volume) -> None:
        response = api_client.get("/api/volumes/")

        assert response.status_code == 200
        assert response.data["count"] == 1

        response_data = response.data["results"][0]
        assert response_data["slug"] == volume_with_issues.slug
        assert response_data["name"] == volume_with_issues.name
        assert response_data["publisher"]["name"] == (
            volume_with_issues.publisher.name if volume_with_issues.publisher else None
        )
        assert response_data["publisher"]["slug"] == (
            volume_with_issues.publisher.slug if volume_with_issues.publisher else None
        )
        assert response_data["short_description"] == volume_with_issues.short_description
        assert response_data["issues_count"] == volume_with_issues.issues.count()

    @staticmethod
    def test_default_ordering_by_start_year(api_client: APIClient, volumes_with_issues: list[Volume]) -> None:
        response = api_client.get("/api/volumes/")

        assert response.status_code == 200
        assert response.data["count"] == len(volumes_with_issues)

        start_years = [item["start_year"] for item in response.data["results"]]
        assert start_years == sorted(start_years, key=lambda x: x if x is not None else 0)

    @staticmethod
    def test_ordering_by_start_year_ascending(api_client: APIClient, volumes_with_issues: list[Volume]) -> None:
        response = api_client.get("/api/volumes/?ordering=start_year")

        assert response.status_code == 200
        start_years = [item["start_year"] for item in response.data["results"]]
        assert start_years == sorted(start_years, key=lambda x: x if x is not None else 0)

    @staticmethod
    def test_ordering_by_start_year_descending(api_client: APIClient, volumes_with_issues: list[Volume]) -> None:
        response = api_client.get("/api/volumes/?ordering=-start_year")

        assert response.status_code == 200
        start_years = [item["start_year"] for item in response.data["results"]]
        assert start_years == sorted(start_years, key=lambda x: x if x is not None else 0, reverse=True)

    @staticmethod
    def test_ordering_by_name_ascending(api_client: APIClient, volumes_with_issues: list[Volume]) -> None:
        response = api_client.get("/api/volumes/?ordering=name")

        assert response.status_code == 200
        names = [item["name"] for item in response.data["results"]]
        assert names == sorted(names)

    @staticmethod
    def test_ordering_by_name_descending(api_client: APIClient, volumes_with_issues: list[Volume]) -> None:
        response = api_client.get("/api/volumes/?ordering=-name")

        assert response.status_code == 200
        names = [item["name"] for item in response.data["results"]]
        assert names == sorted(names, reverse=True)

    @staticmethod
    def test_ordering_by_issues_count_ascending(api_client: APIClient, volumes_with_issues: list[Volume]) -> None:
        response = api_client.get("/api/volumes/?ordering=issues_count")

        assert response.status_code == 200
        issues_counts = [item["issues_count"] for item in response.data["results"]]
        assert issues_counts == sorted(issues_counts)

    @staticmethod
    def test_ordering_by_issues_count_descending(api_client: APIClient, volumes_with_issues: list[Volume]) -> None:
        response = api_client.get("/api/volumes/?ordering=-issues_count")

        assert response.status_code == 200
        issues_counts = [item["issues_count"] for item in response.data["results"]]
        assert issues_counts == sorted(issues_counts, reverse=True)

    @staticmethod
    def test_invalid_ordering_field(api_client: APIClient, volumes_with_issues: list[Volume]) -> None:
        response = api_client.get("/api/volumes/?ordering=invalid_field")

        assert response.status_code == 200
        start_years = [item["start_year"] for item in response.data["results"]]
        assert start_years == sorted(start_years, key=lambda x: x if x is not None else 0)

    @staticmethod
    def test_pagination_invalid_page(api_client: APIClient, volumes_with_issues: list[Volume]) -> None:
        response = api_client.get("/api/volumes/?page=999")

        assert response.status_code == 404


class TestVolumesStarted:
    started_list_keys = {"slug", "display_name", "image", "max_finished_date", "finished_count", "issues_count"}

    @staticmethod
    def _generate_finished_issues(item, usr: User, finished_date_step: int = 0) -> None:
        finish_date = datetime.min + timedelta(days=finished_date_step)
        finished_issues = FinishedIssueFactory.create_batch(size=randrange(1, 5), user=usr, finish_date=finish_date)
        item.issues.set(x.issue for x in finished_issues)

    @staticmethod
    def _generate_unfinished_issue(item) -> None:
        item.issues.add(IssueFactory.create())

    def _create_unfinished(self, user: User) -> list:
        data = VolumeFactory.create_batch(size=randrange(1, 5))
        for num, item in enumerate(data):
            self._generate_finished_issues(item, user, num)
            self._generate_unfinished_issue(item)
        return data

    def _create_finished(self, user: User) -> None:
        data = VolumeFactory.create_batch(size=randrange(1, 5))
        for item in data:
            self._generate_finished_issues(item, user)

    def _create_not_started(self) -> None:
        data = VolumeFactory.create_batch(size=randrange(1, 5))
        for item in data:
            self._generate_unfinished_issue(item)

    @staticmethod
    def test_started_not_authenticated(api_client: APIClient) -> None:
        response = api_client.get("/api/volumes/started/")
        assert response.status_code == 401

    def test_started_authenticated(self, user: User, authenticated_api_client: APIClient) -> None:
        unfinished = self._create_unfinished(user)
        self._create_finished(user)
        self._create_not_started()

        unfinished_slugs = {x.slug for x in unfinished}

        response = authenticated_api_client.get("/api/volumes/started/")
        response_slugs = {x["slug"] for x in response.data["results"]}

        assert response.status_code == 200
        assert len(response.data["results"]) == len(unfinished)
        assert unfinished_slugs == response_slugs

    def test_no_unfinished_authenticated(self, user: User, authenticated_api_client: APIClient) -> None:
        self._create_finished(user)
        self._create_not_started()

        response = authenticated_api_client.get("/api/volumes/started/")

        assert response.status_code == 200
        assert len(response.data["results"]) == 0
        assert response.data["count"] == 0

    def test_started_serializer_fields(self, user: User, authenticated_api_client: APIClient) -> None:
        self._create_unfinished(user)

        response = authenticated_api_client.get("/api/volumes/started/")

        assert response.status_code == 200
        for item in response.data["results"]:
            assert set(item.keys()) == self.started_list_keys
            max_finished_date = item["max_finished_date"]
            if isinstance(max_finished_date, str):
                assert parse_datetime(max_finished_date) is not None
            else:
                assert isinstance(max_finished_date, datetime)

    def test_started_ordering_by_max_finished_date(self, user: User, authenticated_api_client: APIClient) -> None:
        unfinished = self._create_unfinished(user)

        response = authenticated_api_client.get("/api/volumes/started/")

        assert response.status_code == 200

        def max_finished_date(volume: Volume):
            return (
                FinishedIssue.objects.filter(issue__in=volume.issues.all(), user=user).aggregate(Max("finish_date"))[
                    "finish_date__max"
                ]
                or datetime.min
            )

        expected_slugs = [volume.slug for volume in sorted(unfinished, key=max_finished_date, reverse=True)]
        response_slugs = [item["slug"] for item in response.data["results"]]
        assert response_slugs == expected_slugs

    @staticmethod
    def test_started_invalid_page(user: User, authenticated_api_client: APIClient) -> None:
        volumes = VolumeFactory.create_batch(size=3, add_issues=randrange(1, 3))
        for volume in volumes:
            for issue in volume.issues.all():
                issue.finished_users.add(user)
        response = authenticated_api_client.get("/api/volumes/started/?page=999")

        assert response.status_code == 404
