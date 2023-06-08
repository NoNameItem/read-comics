import pytest

pytestmark = pytest.mark.django_db


class TestMissingIssuesE2E:
    # Count tests
    ##########################

    @staticmethod
    def test_count(api_client, missing_issues) -> None:
        response = api_client().get("/api/missing-issues/count/")
        assert response.status_code == 200
        assert response.data["count"] == len(missing_issues)
