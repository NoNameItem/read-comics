import pytest
from rest_framework.test import APIClient

from ..models import MissingIssue

pytestmark = pytest.mark.django_db


class TestMissingIssuesE2E:
    # Count tests
    ##########################

    @staticmethod
    def test_count(api_client: APIClient, missing_issues: list[MissingIssue]) -> None:
        response = api_client.get("/api/missing-issues/count/")
        assert response.status_code == 200
        assert response.data["count"] == len(missing_issues)
