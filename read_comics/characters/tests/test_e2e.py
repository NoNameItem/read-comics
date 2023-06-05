import pytest

from read_comics.utils.test_utils.e2e_mixins import CountTestMixin

from .factories import CharacterFactory

pytestmark = pytest.mark.django_db


class TestCharactersE2E(CountTestMixin):
    factory = CharacterFactory
    count_url = "/api/characters/count/"
