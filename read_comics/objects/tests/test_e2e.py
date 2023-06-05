import pytest

from read_comics.utils.test_utils.e2e_mixins import CountTestMixin

from .factories import ObjectFactory

pytestmark = pytest.mark.django_db


class TestObjectsE2E(CountTestMixin):
    factory = ObjectFactory
    count_url = "/api/objects/count/"
