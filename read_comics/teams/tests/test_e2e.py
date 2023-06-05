import pytest

from read_comics.utils.test_utils.e2e_mixins import CountTestMixin

from .factories import TeamFactory

pytestmark = pytest.mark.django_db


class TestTeamsE2E(CountTestMixin):
    factory = TeamFactory
    count_url = "/api/teams/count/"
