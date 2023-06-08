from random import randrange

import pytest

from ..models import MissingIssue
from .factories import MissingIssueFactory


@pytest.fixture
def missing_issues() -> list[MissingIssue]:
    return MissingIssueFactory.create_batch(size=randrange(2, 10))


@pytest.fixture
def missing_issue() -> MissingIssue:
    return MissingIssueFactory()
