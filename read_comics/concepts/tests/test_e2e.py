import pytest

pytestmark = pytest.mark.django_db


class TestConceptsE2E:
    # Count tests
    ##########################

    @staticmethod
    def test_count(api_client, concepts_no_issues, concepts_with_issues) -> None:
        response = api_client().get("/api/concepts/count/")
        assert response.status_code == 200
        assert response.data["count"] == len(concepts_with_issues)

    @staticmethod
    def test_count_all(api_client, concepts_no_issues, concepts_with_issues) -> None:
        response = api_client().get("/api/concepts/count/?show-all=yes")
        assert response.status_code == 200
        assert response.data["count"] == len(concepts_with_issues) + len(concepts_no_issues)
