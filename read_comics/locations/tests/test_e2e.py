import pytest

from read_comics.utils.test_utils.e2e_mixins import CountTestMixin

from .factories import LocationFactory

pytestmark = pytest.mark.django_db


class TestLocationsE2E(CountTestMixin):
    factory = LocationFactory
    count_url = "/api/locations/count/"
    model_bakery_kwargs = {"slug": None}
