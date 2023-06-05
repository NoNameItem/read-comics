# pylint: skip-file

import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from read_comics.issues.models import Issue
from read_comics.users.models import User
from read_comics.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir) -> None:
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def api_client() -> type:
    return APIClient


@pytest.fixture
def authenticated_api_client(user) -> APIClient:
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    return client


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture(autouse=True)
def stop_s3_update(monkeypatch):
    def update_do_metadata(self, volume_name=None, volume_start_year=None):
        # Override to empty for disable s3 communications in test
        pass

    monkeypatch.setattr(Issue, "update_do_metadata", update_do_metadata)
