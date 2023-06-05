import pytest

from read_comics.utils.test_utils.e2e_mixins import CountTestMixin

from .factories import PublisherFactory

pytestmark = pytest.mark.django_db


class TestPublishersE2E(CountTestMixin):
    factory = PublisherFactory
    count_url = "/api/publishers/count/"
