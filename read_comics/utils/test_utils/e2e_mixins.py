from datetime import datetime, timedelta
from random import randrange

from utils.typing.e2e_test_protocols import CountTestSuite, StartedTestSuite

from read_comics.issues.tests.factories import FinishedIssueFactory, IssueFactory
from read_comics.users.models import User


class CountTestMixin:
    def test_count(self: CountTestSuite, api_client) -> None:
        data: list = self.factory.create_batch(size=randrange(1, 10))
        response = api_client().get(self.count_url)
        assert response.status_code == 200
        assert response.data["count"] == len(data)


class StartedTestMixin:
    @staticmethod
    def _generate_finished_issues(item, usr: User, finished_date_step: int = 0) -> None:
        finish_date = datetime.min + timedelta(days=finished_date_step)
        finished_issues = FinishedIssueFactory.create_batch(size=randrange(1, 5), user=usr, finish_date=finish_date)
        item.issues.add(*map(lambda x: x.issue, finished_issues))

    @staticmethod
    def _generate_unfinished_issue(item) -> None:
        item.issues.add(IssueFactory.create())

    def _create_unfinished(self: StartedTestSuite, user: User) -> list:
        data = self.factory.create_batch(size=randrange(1, 5))
        for num, item in enumerate(data):
            self._generate_finished_issues(item, user, num)
            self._generate_unfinished_issue(item)
        return data

    def _create_finished(self: StartedTestSuite, user: User) -> None:
        data = self.factory.create_batch(size=randrange(1, 5))
        for item in data:
            self._generate_finished_issues(item, user)

    def _create_not_started(self: StartedTestSuite) -> None:
        data = self.factory.create_batch(size=randrange(1, 5))
        for item in data:
            self._generate_unfinished_issue(item)

    def test_started_not_authenticated(self: StartedTestSuite, api_client) -> None:
        response = api_client().get(self.started_url)
        assert response.status_code == 401

    def test_started_authenticated(self: StartedTestSuite, user, authenticated_api_client) -> None:
        unfinished = self._create_unfinished(user)
        self._create_finished(user)
        self._create_not_started()

        unfinished_slugs = set(map(lambda x: x.slug, unfinished))

        response = authenticated_api_client.get(self.started_url)
        response_slugs = set(map(lambda x: x["slug"], response.data["results"]))

        assert response.status_code == 200
        assert len(response.data["results"]) == len(unfinished)
        assert unfinished_slugs == response_slugs

    def test_no_unfinished_authenticated(self: StartedTestSuite, user, authenticated_api_client) -> None:
        self._create_finished(user)
        self._create_not_started()

        response = authenticated_api_client.get(self.started_url)

        assert response.status_code == 200
        assert len(response.data["results"]) == 0
        assert response.data["count"] == 0
