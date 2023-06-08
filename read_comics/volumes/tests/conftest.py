from random import randrange

import pytest

from ..models import Volume
from .factories import VolumeFactory


@pytest.fixture
def volumes_no_issues() -> list[Volume]:
    return VolumeFactory.create_batch(size=randrange(2, 10))


@pytest.fixture
def volumes_with_issues() -> list[Volume]:
    return VolumeFactory.create_batch(size=randrange(2, 10), add_issues=randrange(1, 3))


@pytest.fixture
def volume_with_issues() -> Volume:
    return VolumeFactory(add_issues=randrange(1, 3))


@pytest.fixture
def volume_no_issues() -> Volume:
    return VolumeFactory()
