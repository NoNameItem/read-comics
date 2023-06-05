import pytest

from read_comics.utils.test_utils.e2e_mixins import CountTestMixin

from .factories import MissingIssueFactory

pytestmark = pytest.mark.django_db


class TestMissingIssuesE2E(CountTestMixin):
    factory = MissingIssueFactory
    count_url = "/api/missing-issues/count/"
