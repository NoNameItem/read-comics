from rest_framework import serializers

from ..models import Publisher


class NestedPublisherSerializer(serializers.ModelSerializer):
    image = serializers.ReadOnlyField(source="square_avatar")

    class Meta:
        model = Publisher
        fields = ["name", "image", "slug"]
