from datetime import datetime, timedelta
from random import randrange

import pytest
from issues.tests.factories import FinishedIssueFactory, IssueFactory
from rest_framework.test import APIClient

from read_comics.users.models import User

from ..models import Volume
from .factories import VolumeFactory

pytestmark = pytest.mark.django_db


class TestVolumesE2E:
    # Count tests
    ##########################

    @staticmethod
    def test_count(api_client: APIClient, volumes_no_issues: list[Volume], volumes_with_issues: list[Volume]) -> None:
        response = api_client.get("/api/volumes/count/")
        assert response.status_code == 200
        assert response.data["count"] == len(volumes_with_issues)

    @staticmethod
    def test_count_all(
        api_client: APIClient, volumes_no_issues: list[Volume], volumes_with_issues: list[Volume]
    ) -> None:
        response = api_client.get("/api/volumes/count/?show-all=yes")
        assert response.status_code == 200
        assert response.data["count"] == len(volumes_with_issues) + len(volumes_no_issues)

    # Started tests
    ##########################

    @staticmethod
    def _generate_finished_issues(item, usr: User, finished_date_step: int = 0) -> None:
        finish_date = datetime.min + timedelta(days=finished_date_step)
        finished_issues = FinishedIssueFactory.create_batch(size=randrange(1, 5), user=usr, finish_date=finish_date)
        item.issues.add(*map(lambda x: x.issue, finished_issues))

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

        unfinished_slugs = set(map(lambda x: x.slug, unfinished))

        response = authenticated_api_client.get("/api/volumes/started/")
        response_slugs = set(map(lambda x: x["slug"], response.data["results"]))

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
