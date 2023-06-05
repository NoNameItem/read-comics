import pytest

from read_comics.utils.test_utils.e2e_mixins import CountTestMixin, StartedTestMixin

from .factories import VolumeFactory

pytestmark = pytest.mark.django_db


class TestVolumesE2E(CountTestMixin, StartedTestMixin):
    factory = VolumeFactory

    count_url = "/api/volumes/count/"
    started_url = "/api/volumes/started/"
