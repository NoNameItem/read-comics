import pytest

pytestmark = pytest.mark.django_db


class TestPeopleE2E:
    # Count tests
    ##########################

    @staticmethod
    def test_count(api_client, people_no_issues, people_with_issues) -> None:
        response = api_client().get("/api/people/count/")
        assert response.status_code == 200
        assert response.data["count"] == len(people_with_issues)

    @staticmethod
    def test_count_all(api_client, people_no_issues, people_with_issues) -> None:
        response = api_client().get("/api/people/count/?show-all=yes")
        assert response.status_code == 200
        assert response.data["count"] == len(people_with_issues) + len(people_no_issues)
