from random import randrange

import pytest

from ..models import Team
from .factories import TeamFactory


@pytest.fixture
def teams_no_issues() -> list[Team]:
    return TeamFactory.create_batch(size=randrange(2, 10))


@pytest.fixture
def teams_with_issues() -> list[Team]:
    return TeamFactory.create_batch(size=randrange(2, 10), add_issues=randrange(1, 3))


@pytest.fixture
def team_with_issues() -> Team:
    return TeamFactory(add_issues=randrange(1, 3))


@pytest.fixture
def team_no_issues() -> Team:
    return TeamFactory()
