import pytest

from read_comics.utils.test_utils.e2e_mixins import CountTestMixin, StartedTestMixin

from ..tests.factories import StoryArcFactory

pytestmark = pytest.mark.django_db


class TestStoryArcsE2E(CountTestMixin, StartedTestMixin):
    factory = StoryArcFactory
    count_url = "/api/story-arcs/count/"
    started_url = "/api/story-arcs/started/"
