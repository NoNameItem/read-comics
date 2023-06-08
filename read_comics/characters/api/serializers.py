from rest_framework import serializers

from read_comics.publishers.api.serializers import NestedPublisherSerializer

from ..models import Character


class CharactersListSerializer(serializers.ModelSerializer):
    image = serializers.ReadOnlyField(source="square_medium")
    publisher = NestedPublisherSerializer(read_only=True)
    issues_count = serializers.ReadOnlyField()
    volumes_count = serializers.ReadOnlyField()

    class Meta:
        model = Character
        fields = ["slug", "image", "publisher", "name", "short_description", "issues_count", "volumes_count"]
