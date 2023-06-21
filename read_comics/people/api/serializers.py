from rest_framework import serializers

from ..models import Person


class PeopleListSerializer(serializers.ModelSerializer):
    image = serializers.ReadOnlyField(source="square_medium")
    issues_count = serializers.ReadOnlyField()
    volumes_count = serializers.ReadOnlyField()

    class Meta:
        model = Person
        fields = ["slug", "image", "name", "short_description", "issues_count", "volumes_count"]
