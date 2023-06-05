from django.urls import resolve, reverse
from utils.typing.api_url_test_protocols import APIUrlTest


class CountAPIUrlTestMixin:
    def test_count(self: APIUrlTest) -> None:
        assert reverse(f"api:{self.base_name}-count") == f"/api/{self.base_url}/count/"
        assert resolve(f"/api/{self.base_url}/count/").view_name == f"api:{self.base_name}-count"


class StartedAPIUrlTestMixin:
    def test_started(self: APIUrlTest) -> None:
        assert reverse(f"api:{self.base_name}-started") == f"/api/{self.base_url}/started/"
        assert resolve(f"/api/{self.base_url}/started/").view_name == f"api:{self.base_name}-started"
