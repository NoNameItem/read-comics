from datetime import datetime, timedelta
from random import randrange

import pytest
from issues.tests.factories import FinishedIssueFactory, IssueFactory

from read_comics.users.models import User

from ..tests.factories import StoryArcFactory

pytestmark = pytest.mark.django_db


class TestStoryArcsE2E:
    # Count tests
    ##########################

    @staticmethod
    def test_count(api_client, story_arcs_no_issues, story_arcs_with_issues) -> None:
        response = api_client().get("/api/story-arcs/count/")
        assert response.status_code == 200
        assert response.data["count"] == len(story_arcs_with_issues)

    @staticmethod
    def test_count_all(api_client, story_arcs_no_issues, story_arcs_with_issues) -> None:
        response = api_client().get("/api/story-arcs/count/?show-all=yes")
        assert response.status_code == 200
        assert response.data["count"] == len(story_arcs_with_issues) + len(story_arcs_no_issues)

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
        data = StoryArcFactory.create_batch(size=randrange(1, 5))
        for num, item in enumerate(data):
            self._generate_finished_issues(item, user, num)
            self._generate_unfinished_issue(item)
        return data

    def _create_finished(self, user: User) -> None:
        data = StoryArcFactory.create_batch(size=randrange(1, 5))
        for item in data:
            self._generate_finished_issues(item, user)

    def _create_not_started(self) -> None:
        data = StoryArcFactory.create_batch(size=randrange(1, 5))
        for item in data:
            self._generate_unfinished_issue(item)

    @staticmethod
    def test_started_not_authenticated(api_client) -> None:
        response = api_client().get("/api/story-arcs/started/")
        assert response.status_code == 401

    def test_started_authenticated(self, user, authenticated_api_client) -> None:
        unfinished = self._create_unfinished(user)
        self._create_finished(user)
        self._create_not_started()

        unfinished_slugs = set(map(lambda x: x.slug, unfinished))

        response = authenticated_api_client.get("/api/story-arcs/started/")
        response_slugs = set(map(lambda x: x["slug"], response.data["results"]))

        assert response.status_code == 200
        assert len(response.data["results"]) == len(unfinished)
        assert unfinished_slugs == response_slugs

    def test_no_unfinished_authenticated(self, user, authenticated_api_client) -> None:
        self._create_finished(user)
        self._create_not_started()

        response = authenticated_api_client.get("/api/story-arcs/started/")

        assert response.status_code == 200
        assert len(response.data["results"]) == 0
        assert response.data["count"] == 0
