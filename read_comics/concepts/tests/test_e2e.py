import pytest

from read_comics.utils.test_utils.e2e_mixins import CountTestMixin

from .factories import ConceptFactory

pytestmark = pytest.mark.django_db


class TestConceptsE2E(CountTestMixin):
    factory = ConceptFactory
    count_url = "/api/concepts/count/"
