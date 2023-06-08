import pytest

pytestmark = pytest.mark.django_db


class TestIssuesE2E:
    # Count tests
    ##########################

    @staticmethod
    def test_count(api_client, issues) -> None:
        response = api_client().get("/api/issues/count/")
        assert response.status_code == 200
        assert response.data["count"] == len(issues)
