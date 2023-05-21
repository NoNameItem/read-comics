from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.settings import api_settings

from read_comics.utils.api.serializer_mixins import CurrentUserMixin

User = get_user_model()


class ThumbnailImageField(serializers.ImageField):
    def to_representation(self, value):
        if not value:
            return None

        use_url = getattr(self, "use_url", api_settings.UPLOADED_FILES_USE_URL)
        if use_url:
            try:
                url = value.url
                thumb_url = value.thumb_url
            except AttributeError:
                return None
            request = self.context.get("request", None)
            if request is not None:
                return {"image": request.build_absolute_uri(url), "thumbnail": request.build_absolute_uri(thumb_url)}
            return {"image": url, "thumbnail": thumb_url}

        return {"image": value.name, "thumbnail": value.thumb_name}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "name", "url", "image_thumb_url", "last_active"]

        extra_kwargs = {"url": {"view_name": "api:user-detail", "lookup_field": "username"}}


class UserLoginSerializer(serializers.ModelSerializer):
    images = ThumbnailImageField(source="_user_image")

    class Meta:
        model = User
        fields = ["username", "name", "images", "email", "email_verified", "is_superuser", "is_staff", "gender"]


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
