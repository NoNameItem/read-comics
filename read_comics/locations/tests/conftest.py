from random import randrange

import pytest

from ..models import Location
from .factories import LocationFactory


@pytest.fixture
def locations_no_issues() -> list[Location]:
    return LocationFactory.create_batch(size=randrange(2, 10))


@pytest.fixture
def locations_with_issues() -> list[Location]:
    return LocationFactory.create_batch(size=randrange(2, 10), add_issues=randrange(1, 3))


@pytest.fixture
def location_with_issues() -> Location:
    return LocationFactory(add_issues=randrange(1, 3))


@pytest.fixture
def location_no_issues() -> Location:
    return LocationFactory()
