from django.urls import resolve, reverse


class TestUserApiUrls:
    @staticmethod
    def test_login() -> None:
        assert reverse("rest_login") == "/api/auth/login/"
        assert resolve("/api/auth/login/").view_name == "rest_login"

    @staticmethod
    def test_refresh_token() -> None:
        assert reverse("token_refresh") == "/api/auth/token/refresh/"
        assert resolve("/api/auth/token/refresh/").view_name == "token_refresh"

    @staticmethod
    def test_register() -> None:
        assert reverse("rest_register") == "/api/auth/registration/"
        assert resolve("/api/auth/registration/").view_name == "rest_register"

    @staticmethod
    def test_confirm_email() -> None:
        assert reverse("rest_verify_email") == "/api/auth/registration/verify-email/"
        assert resolve("/api/auth/registration/verify-email/").view_name == "rest_verify_email"

    @staticmethod
    def test_resend_email() -> None:
        assert reverse("rest_resend_email") == "/api/auth/registration/resend-email/"
        assert resolve("/api/auth/registration/resend-email/").view_name == "rest_resend_email"

    @staticmethod
    def test_reset_password() -> None:
        assert reverse("rest_password_reset") == "/api/auth/password/reset/"
        assert resolve("/api/auth/password/reset/").view_name == "rest_password_reset"

    @staticmethod
    def test_reset_password_confirm() -> None:
        assert reverse("rest_password_reset_confirm") == "/api/auth/password/reset/confirm/"
        assert resolve("/api/auth/password/reset/confirm/").view_name == "rest_password_reset_confirm"

    @staticmethod
    def test_password_change() -> None:
        assert reverse("rest_password_change") == "/api/auth/password/change/"
        assert resolve("/api/auth/password/change/").view_name == "rest_password_change"

    @staticmethod
    def test_profile() -> None:
        assert reverse("profile") == "/api/profile/"
        assert resolve("/api/profile/").view_name == "profile"

    @staticmethod
    def test_finished_stats() -> None:
        assert reverse("finished_stats") == "/api/profile/finished-stats/"
        assert resolve("/api/profile/finished-stats/").view_name == "finished_stats"

    @staticmethod
    def test_change_email() -> None:
        assert reverse("change_email") == "/api/profile/change-email/"
        assert resolve("/api/profile/change-email/").view_name == "change_email"
