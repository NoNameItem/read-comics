from random import randrange

import pytest

from ..models import Object
from .factories import ObjectFactory


@pytest.fixture
def objects_no_issues() -> list[Object]:
    return ObjectFactory.create_batch(size=randrange(2, 10))


@pytest.fixture
def objects_with_issues() -> list[Object]:
    return ObjectFactory.create_batch(size=randrange(2, 10), add_issues=randrange(1, 3))


@pytest.fixture
def object_with_issues() -> Object:
    return ObjectFactory(add_issues=randrange(1, 3))


@pytest.fixture
def object_no_issues() -> Object:
    return ObjectFactory()
