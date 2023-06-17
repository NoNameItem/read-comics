from random import randrange

import pytest

from ..models import Issue
from .factories import FinishedIssueFactory, IssueFactory


@pytest.fixture
def issues() -> list[Issue]:
    return IssueFactory.create_batch(size=randrange(2, 10))


@pytest.fixture
def issue() -> Issue:
    return IssueFactory()


@pytest.fixture
def finished_issues(user) -> list[Issue]:
    finished_issues = FinishedIssueFactory.create_batch(size=randrange(2, 10), user=user)
    return [x.issue for x in finished_issues]


@pytest.fixture
def finished_issue(user) -> Issue:
    finished_issue = FinishedIssueFactory(user=user)
    return finished_issue.issue
