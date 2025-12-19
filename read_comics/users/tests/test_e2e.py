from datetime import timedelta

import pytest
from allauth.account.models import EmailAddress
from django.utils import timezone
from factory import Iterator
from rest_framework.test import APIClient

from read_comics.issues.tests.factories import FinishedIssueFactory
from read_comics.users.models import User
from read_comics.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestProfileView:
    @staticmethod
    def test_requires_auth(api_client: APIClient) -> None:
        response = api_client.get("/api/profile/")

        assert response.status_code == 401

    @staticmethod
    def test_get_returns_profile(authenticated_api_client: APIClient, user: User) -> None:
        EmailAddress.objects.create(user=user, email=user.email, primary=True, verified=True)
        FinishedIssueFactory.create_batch(2, user=user, finish_date=timezone.now())

        response = authenticated_api_client.get("/api/profile/")

        assert response.status_code == 200
        assert response.data["username"] == user.username
        assert response.data["email"] == user.email
        assert response.data["email_verified"] is True
        assert response.data["finished_count"] == 2
        assert float(response.data["reading_speed"]) == 2.0

    @staticmethod
    def test_patch_updates_writable_fields(authenticated_api_client: APIClient, user: User) -> None:
        EmailAddress.objects.create(user=user, email=user.email, primary=True, verified=True)

        response = authenticated_api_client.patch(
            "/api/profile/",
            {"name": "New Name", "bio": "New bio", "gender": "M"},
            format="json",
        )

        assert response.status_code == 200
        user.refresh_from_db()
        assert user.name == "New Name"
        assert user.bio == "New bio"
        assert user.gender == "M"

    @staticmethod
    def test_patch_ignores_read_only_fields(authenticated_api_client: APIClient, user: User) -> None:
        EmailAddress.objects.create(user=user, email=user.email, primary=True, verified=True)
        FinishedIssueFactory(user=user, finish_date=timezone.now())

        response = authenticated_api_client.patch(
            "/api/profile/",
            {"username": "new-username", "email": "new@example.com", "finished_count": 99, "name": "Keep"},
            format="json",
        )

        assert response.status_code == 200
        user.refresh_from_db()
        assert user.username != "new-username"
        assert user.email != "new@example.com"
        assert response.data["finished_count"] == 1

    @staticmethod
    def test_patch_rejects_unknown_field(authenticated_api_client: APIClient, user: User) -> None:
        EmailAddress.objects.create(user=user, email=user.email, primary=True, verified=True)

        response = authenticated_api_client.patch(
            "/api/profile/",
            {"unknown_field": "value"},
            format="json",
        )

        assert response.status_code == 400
        assert "unknown_field" in response.data


class TestFinishedIssuesStatsView:
    @staticmethod
    def test_requires_auth(api_client: APIClient) -> None:
        response = api_client.get("/api/profile/finished-stats/")

        assert response.status_code == 401

    @staticmethod
    def test_returns_stats(authenticated_api_client: APIClient, user: User) -> None:
        today = timezone.now()
        FinishedIssueFactory.create_batch(2, user=user, finish_date=Iterator([today, today - timedelta(days=1)]))

        response = authenticated_api_client.get("/api/profile/finished-stats/")

        assert response.status_code == 200
        assert response.data["finished_count"] == 2
        assert response.data["today_finished_count"] == 1
        assert float(response.data["reading_speed"]) == 1.0


class TestChangeEmailView:
    @staticmethod
    def test_requires_auth(api_client: APIClient) -> None:
        response = api_client.patch("/api/profile/change-email/", {"email": "new@example.com"}, format="json")

        assert response.status_code == 401

    @staticmethod
    def test_updates_email(authenticated_api_client: APIClient, user: User) -> None:
        email_address = EmailAddress.objects.create(user=user, email=user.email, primary=True, verified=True)

        response = authenticated_api_client.patch(
            "/api/profile/change-email/",
            {"email": "new@example.com"},
            format="json",
        )

        assert response.status_code == 200
        email_address.refresh_from_db()
        assert email_address.email == "new@example.com"
        assert response.data["email"] == "new@example.com"

    @staticmethod
    def test_rejects_duplicate_email(authenticated_api_client: APIClient, user: User) -> None:
        EmailAddress.objects.create(user=user, email=user.email, primary=True, verified=True)
        other_user = UserFactory(email="used@example.com")
        EmailAddress.objects.create(user=other_user, email=other_user.email, primary=True, verified=True)

        response = authenticated_api_client.patch(
            "/api/profile/change-email/",
            {"email": "used@example.com"},
            format="json",
        )

        assert response.status_code == 400
        assert response.data["email"][0] == "User with this e-mail address already exists."

    @staticmethod
    def test_verified_field_is_read_only(authenticated_api_client: APIClient, user: User) -> None:
        email_address = EmailAddress.objects.create(user=user, email=user.email, primary=True, verified=False)

        response = authenticated_api_client.patch(
            "/api/profile/change-email/",
            {"email": user.email, "verified": True},
            format="json",
        )

        assert response.status_code == 200
        email_address.refresh_from_db()
        assert email_address.verified is False
