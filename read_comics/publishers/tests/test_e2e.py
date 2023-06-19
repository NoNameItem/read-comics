import pytest
from rest_framework.test import APIClient

from ..models import Publisher

pytestmark = pytest.mark.django_db


class TestPublishersE2E:
    # Count tests
    ##########################

    @staticmethod
    def test_count(
        api_client: APIClient, publishers_no_volumes: list[Publisher], publishers_with_volumes: list[Publisher]
    ) -> None:
        response = api_client.get("/api/publishers/count/")
        assert response.status_code == 200
        assert response.data["count"] == len(publishers_with_volumes)

    @staticmethod
    def test_count_all(
        api_client: APIClient, publishers_no_volumes: list[Publisher], publishers_with_volumes: list[Publisher]
    ) -> None:
        response = api_client.get("/api/publishers/count/?show-all=yes")
        assert response.status_code == 200
        assert response.data["count"] == len(publishers_with_volumes) + len(publishers_no_volumes)
