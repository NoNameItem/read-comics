import pytest

from read_comics.utils.test_utils.e2e_mixins import CountTestMixin

from .factories import IssueFactory

pytestmark = pytest.mark.django_db


class TestIssuesE2E(CountTestMixin):
    factory = IssueFactory
    count_url = "/api/issues/count/"
