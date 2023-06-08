import pytest

pytestmark = pytest.mark.django_db


class TestLocationsE2E:
    # Count tests
    ##########################

    @staticmethod
    def test_count(api_client, locations_no_issues, locations_with_issues) -> None:
        response = api_client().get("/api/locations/count/")
        assert response.status_code == 200
        assert response.data["count"] == len(locations_with_issues)

    @staticmethod
    def test_count_all(api_client, locations_no_issues, locations_with_issues) -> None:
        response = api_client().get("/api/locations/count/?show-all=yes")
        assert response.status_code == 200
        assert response.data["count"] == len(locations_with_issues) + len(locations_no_issues)
