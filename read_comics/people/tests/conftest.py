from random import randrange

import pytest

from ..models import Person
from .factories import PersonFactory


@pytest.fixture
def people_no_issues() -> list[Person]:
    return PersonFactory.create_batch(size=randrange(2, 10))


@pytest.fixture
def people_with_issues() -> list[Person]:
    return PersonFactory.create_batch(size=randrange(2, 10), add_issues=randrange(1, 3))


@pytest.fixture
def person_with_issues() -> Person:
    return PersonFactory(add_issues=randrange(1, 3))


@pytest.fixture
def person_no_issues() -> Person:
    return PersonFactory()
