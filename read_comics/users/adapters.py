from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.contrib.messages.constants import DEFAULT_LEVELS as DJANGO_DEFAULT_LEVELS
from django.http import HttpRequest
from django.urls import reverse
from django_magnificent_messages.constants import DEFAULT_LEVELS as DMM_DEFAULT_LEVELS


class AccountAdapter(DefaultAccountAdapter):
    MESSAGE_LEVEL_MAPPING = {
        DJANGO_DEFAULT_LEVELS["DEBUG"]: DMM_DEFAULT_LEVELS["SECONDARY"],
        DJANGO_DEFAULT_LEVELS["INFO"]: DMM_DEFAULT_LEVELS["INFO"],
        DJANGO_DEFAULT_LEVELS["SUCCESS"]: DMM_DEFAULT_LEVELS["SUCCESS"],
        DJANGO_DEFAULT_LEVELS["WARNING"]: DMM_DEFAULT_LEVELS["WARNING"],
        DJANGO_DEFAULT_LEVELS["ERROR"]: DMM_DEFAULT_LEVELS["ERROR"],
    }

    def is_open_for_signup(self, request: HttpRequest):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def get_email_confirmation_url(self, request, emailconfirmation):
        """Constructs the email confirmation (activation) url.

        Note that if you have architected your system such that email
        confirmations are sent outside of the request context `request`
        can be `None` here.
        """
        return f"{settings.FRONTEND_BASE_URL}/confirm-email?key={emailconfirmation.key}"


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest, sociallogin: Any):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def get_connect_redirect_url(self, request, socialaccount):
        assert request.user.is_authenticated
        return reverse("users:edit") + "?show_tab=social"
