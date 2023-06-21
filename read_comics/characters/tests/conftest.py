from random import randrange

import pytest

from ..models import Character
from .factories import CharacterFactory


@pytest.fixture
def characters_no_issues() -> list[Character]:
    return CharacterFactory.create_batch(size=randrange(2, 10))


@pytest.fixture
def characters_with_issues() -> list[Character]:
    return CharacterFactory.create_batch(size=randrange(2, 10), add_issues=randrange(1, 3))


@pytest.fixture
def character_with_issues() -> Character:
    return CharacterFactory(add_issues=randrange(1, 3))


@pytest.fixture
def character_no_issues() -> Character:
    return CharacterFactory()
