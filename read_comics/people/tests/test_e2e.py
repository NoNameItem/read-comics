import pytest

from read_comics.utils.test_utils.e2e_mixins import CountTestMixin

from .factories import PersonFactory

pytestmark = pytest.mark.django_db


class TestPeopleE2E(CountTestMixin):
    factory = PersonFactory
    count_url = "/api/people/count/"
