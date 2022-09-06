from django.contrib.auth import get_user_model
from rest_framework import serializers

from read_comics.utils.api.serializer_mixins import CurrentUserMixin

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "name", "url", "image_thumb_url", "last_active"]

        extra_kwargs = {"url": {"view_name": "api:user-detail", "lookup_field": "username"}}


class UserDetailSerializer(CurrentUserMixin, serializers.ModelSerializer):
    email = serializers.SerializerMethodField()

    def get_email(self, obj):
        if obj.show_email:
            return obj.email

        current_user = self.current_user
        if current_user and current_user.is_authenticated and current_user.id == obj.id:
            return obj.email
        return None

    class Meta:
        model = User
        fields = [
            "username",
            "name",
            "url",
            "image_thumb_url",
            "image_url",
            "gender",
            "birth_date",
            "email",
            "last_active",
            "bio",
            "is_superuser",
            "is_staff",
            "is_active",
        ]

        extra_kwargs = {"url": {"view_name": "api:user-detail", "lookup_field": "username"}}
