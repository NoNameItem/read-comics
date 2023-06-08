from random import randrange

import pytest

from ..models import StoryArc
from .factories import StoryArcFactory


@pytest.fixture
def story_arcs_no_issues() -> list[StoryArc]:
    return StoryArcFactory.create_batch(size=randrange(2, 10))


@pytest.fixture
def story_arcs_with_issues() -> list[StoryArc]:
    return StoryArcFactory.create_batch(size=randrange(2, 10), add_issues=randrange(1, 3))


@pytest.fixture
def story_arc_with_issues() -> StoryArc:
    return StoryArcFactory(add_issues=randrange(1, 3))


@pytest.fixture
def story_arc_no_issues() -> StoryArc:
    return StoryArcFactory()
