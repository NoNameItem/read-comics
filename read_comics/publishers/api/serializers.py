from rest_framework import serializers

from ..models import Publisher


class NestedPublisherSerializer(serializers.ModelSerializer):
    image = serializers.ReadOnlyField(source="square_avatar")

    class Meta:
        model = Publisher
        fields = ["name", "image", "slug"]


class PublishersListSerializer(serializers.ModelSerializer):
    image = serializers.ReadOnlyField(source="square_medium")
    issues_count = serializers.ReadOnlyField()
    volumes_count = serializers.ReadOnlyField()

    class Meta:
        model = Publisher
        fields = ["slug", "image", "name", "short_description", "issues_count", "volumes_count"]
