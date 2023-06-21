from random import randrange

import pytest

from ..models import Publisher
from .factories import PublisherFactory


@pytest.fixture
def publishers_no_volumes() -> list[Publisher]:
    return PublisherFactory.create_batch(size=randrange(2, 10))


@pytest.fixture
def publishers_with_volumes() -> list[Publisher]:
    return PublisherFactory.create_batch(size=randrange(2, 10), add_volumes=randrange(1, 3))


@pytest.fixture
def publisher_with_volumes() -> Publisher:
    return PublisherFactory(add_volumes=randrange(1, 3))


@pytest.fixture
def publisher_no_volumes() -> Publisher:
    return PublisherFactory()
