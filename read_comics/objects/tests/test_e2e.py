import pytest

pytestmark = pytest.mark.django_db


class TestObjectsE2E:
    # Count tests
    ##########################

    @staticmethod
    def test_count(api_client, objects_no_issues, objects_with_issues) -> None:
        response = api_client().get("/api/objects/count/")
        assert response.status_code == 200
        assert response.data["count"] == len(objects_with_issues)

    @staticmethod
    def test_count_all(api_client, objects_no_issues, objects_with_issues) -> None:
        response = api_client().get("/api/objects/count/?show-all=yes")
        assert response.status_code == 200
        assert response.data["count"] == len(objects_with_issues) + len(objects_no_issues)
