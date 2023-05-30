from typing import Any

from allauth.account.models import EmailAddress
from allauth.account.utils import user_pk_to_url_str
from dj_rest_auth.serializers import PasswordResetSerializer
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers, validators

from read_comics.users.models import User
from read_comics.utils.api.serializer_fields import NestedChoiceField, ThumbnailImageField

user_model = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_model
        fields = ["username", "name", "url", "image_thumb_url", "last_active"]

        extra_kwargs = {"url": {"view_name": "api:user-detail", "lookup_field": "username"}}


class UserLoginSerializer(serializers.ModelSerializer):
    images = ThumbnailImageField(source="_user_image")
    gender = NestedChoiceField(User.Gender.choices)

    class Meta:
        model = user_model
        fields = [
            "username",
            "name",
            "images",
            "email",
            "email_verified",
            "is_superuser",
            "is_staff",
            "gender",
            "birth_date",
            "date_joined",
        ]


def password_reset_url_generator(request, user, temp_key) -> str:
    return (
        f"{settings.FRONTEND_BASE_URL}/password-reset-confirm"
        f"?uid={user_pk_to_url_str(user)}&token={temp_key}&email={user.email}"
    )


class ResetPasswordSerializer(PasswordResetSerializer):
    def get_email_options(self) -> dict:
        """Override this method to change default e-mail options"""
        return {"url_generator": password_reset_url_generator}


class ProfileSerializer(serializers.ModelSerializer):
    images = ThumbnailImageField(source="_user_image", allow_null=True)
    gender = NestedChoiceField(User.Gender.choices)

    class Meta:
        model = User
        fields = [
            "username",
            "name",
            "images",
            "gender",
            "email",
            "email_verified",
            "bio",
            "finished_count",
            "birth_date",
            "date_joined",
            "reading_speed",
        ]
        read_only_fields = ["username", "date_joined", "email", "email_verified", "finished_count", "reading_speed"]


class ChangeEmailSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # Find UniqueValidator and set custom message
        for validator in self.fields["email"].validators:
            if isinstance(validator, validators.UniqueValidator):
                validator.message = "User with this e-mail address already exists."

    def update(self, instance: EmailAddress, validated_data: Any) -> EmailAddress:
        request = self.context["request"]
        email = validated_data["email"]
        if instance.email != email:
            instance.change(request, email)
        return instance

    class Meta:
        model = EmailAddress
        fields = ["email", "verified"]
        read_only_fields = ["verified"]
