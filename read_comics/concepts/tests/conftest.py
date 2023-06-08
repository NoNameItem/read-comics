from random import randrange

import pytest

from ..models import Concept
from .factories import ConceptFactory


@pytest.fixture
def concepts_no_issues() -> list[Concept]:
    return ConceptFactory.create_batch(size=randrange(2, 10))


@pytest.fixture
def concepts_with_issues() -> list[Concept]:
    return ConceptFactory.create_batch(size=randrange(2, 10), add_issues=randrange(1, 3))


@pytest.fixture
def concept_with_issues() -> Concept:
    return ConceptFactory(add_issues=randrange(1, 3))


@pytest.fixture
def concept_no_issues() -> Concept:
    return ConceptFactory()
