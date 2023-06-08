import pytest

pytestmark = pytest.mark.django_db


class TestTeamsE2E:
    # Count tests
    ##########################

    @staticmethod
    def test_count(api_client, teams_no_issues, teams_with_issues) -> None:
        response = api_client().get("/api/teams/count/")
        assert response.status_code == 200
        assert response.data["count"] == len(teams_with_issues)

    @staticmethod
    def test_count_all(api_client, teams_no_issues, teams_with_issues) -> None:
        response = api_client().get("/api/teams/count/?show-all=yes")
        assert response.status_code == 200
        assert response.data["count"] == len(teams_with_issues) + len(teams_no_issues)
