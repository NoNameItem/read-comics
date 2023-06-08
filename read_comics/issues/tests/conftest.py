from random import randrange

import pytest

from ..models import Issue
from .factories import IssueFactory


@pytest.fixture
def issues() -> list[Issue]:
    return IssueFactory.create_batch(size=randrange(2, 10))


@pytest.fixture
def issue() -> Issue:
    return IssueFactory()
