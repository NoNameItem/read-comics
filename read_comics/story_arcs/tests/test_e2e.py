from datetime import datetime, timedelta
from random import randrange

import pytest
from django.db.models import Count
from issues.tests.factories import FinishedIssueFactory, IssueFactory
from rest_framework.test import APIClient
from utils.utils import flatten_dict

from read_comics.users.models import User

from ..models import StoryArc
from ..tests.factories import StoryArcFactory

pytestmark = pytest.mark.django_db


class TestStoryArcsCount:
    @staticmethod
    def test_count(
        api_client: APIClient,
        story_arcs_no_issues: list[StoryArc],
        story_arcs_with_issues: list[StoryArc],
        finished_story_arcs: list[StoryArc],
    ) -> None:
        response = api_client.get("/api/story-arcs/count/")
        assert response.status_code == 200
        assert response.data["count"] == len(story_arcs_with_issues) + len(story_arcs_no_issues) + len(
            finished_story_arcs
        )


class TestStoryArcsList:
    list_keys = {
        "slug",
        "image",
        "publisher__name",
        "publisher__image",
        "publisher__slug",
        "name",
        "short_description",
        "issues_count",
        "volumes_count",
        "finished_count",
        "is_finished",
    }

    def test_dont_hide_finished(
        self,
        user: User,
        authenticated_api_client: APIClient,
        story_arcs_with_issues: list[StoryArc],
        finished_story_arcs: list[StoryArc],
    ) -> None:
        response = authenticated_api_client.get("/api/story-arcs/?hide-finished=no")

        assert response.status_code == 200
        assert response.data["count"] == len(story_arcs_with_issues) + len(finished_story_arcs)

        flatten_response_data = [flatten_dict(response_item) for response_item in response.data["results"]]
        for item in flatten_response_data:
            assert self.list_keys == set(item.keys())

    def test_hide_finished(
        self,
        user: User,
        authenticated_api_client: APIClient,
        story_arcs_with_issues: list[StoryArc],
        finished_story_arcs: list[StoryArc],
    ) -> None:
        response = authenticated_api_client.get("/api/story-arcs/")

        assert response.status_code == 200
        assert response.data["count"] == len(story_arcs_with_issues)

        flatten_response_data = [flatten_dict(response_item) for response_item in response.data["results"]]
        for item in flatten_response_data:
            assert self.list_keys == set(item.keys())

    @staticmethod
    def test_finished_mark(user: User, authenticated_api_client: APIClient, finished_story_arc: StoryArc) -> None:
        response = authenticated_api_client.get("/api/story-arcs/?hide-finished=no")
        response_data = response.data["results"][0]
        assert response_data["is_finished"]

    @staticmethod
    def test_no_finished_mark(user: User, authenticated_api_client: APIClient, story_arc_with_issues: StoryArc) -> None:
        response = authenticated_api_client.get("/api/story-arcs/")
        response_data = response.data["results"][0]
        assert not response_data["is_finished"]

    @staticmethod
    def test_no_auth_finished_mark(
        api_client: APIClient, story_arc_with_issues: StoryArc, finished_story_arc: StoryArc
    ) -> None:
        response = api_client.get("/api/story-arcs/")
        for response_issue in response.data["results"]:
            assert response_issue["is_finished"] is None

    @staticmethod
    def test_data(api_client: APIClient, story_arc_with_issues: StoryArc) -> None:
        response = api_client.get("/api/story-arcs/")

        assert response.status_code == 200
        assert response.data["count"] == 1

        response_data = response.data["results"][0]
        assert response_data["slug"] == story_arc_with_issues.slug
        assert response_data["name"] == story_arc_with_issues.name
        assert response_data["publisher"]["name"] == (
            story_arc_with_issues.publisher.name if story_arc_with_issues.publisher else None
        )
        assert response_data["publisher"]["slug"] == (
            story_arc_with_issues.publisher.slug if story_arc_with_issues.publisher else None
        )
        assert response_data["short_description"] == story_arc_with_issues.short_description
        assert response_data["issues_count"] == story_arc_with_issues.issues.count()
        assert (
            response_data["volumes_count"]
            == story_arc_with_issues.issues.aggregate(v=Count("volume", distinct=True))["v"]
        )


class TestStoryArcsStarted:
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
    def test_started_not_authenticated(api_client: APIClient) -> None:
        response = api_client.get("/api/story-arcs/started/")
        assert response.status_code == 401

    def test_started_authenticated(self, user: User, authenticated_api_client: APIClient) -> None:
        unfinished = self._create_unfinished(user)
        self._create_finished(user)
        self._create_not_started()

        unfinished_slugs = set(map(lambda x: x.slug, unfinished))

        response = authenticated_api_client.get("/api/story-arcs/started/")
        response_slugs = set(map(lambda x: x["slug"], response.data["results"]))

        assert response.status_code == 200
        assert len(response.data["results"]) == len(unfinished)
        assert unfinished_slugs == response_slugs

    def test_no_unfinished_authenticated(self, user: User, authenticated_api_client: APIClient) -> None:
        self._create_finished(user)
        self._create_not_started()

        response = authenticated_api_client.get("/api/story-arcs/started/")

        assert response.status_code == 200
        assert len(response.data["results"]) == 0
        assert response.data["count"] == 0
