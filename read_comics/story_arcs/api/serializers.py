from rest_framework import serializers

from read_comics.publishers.api.serializers import NestedPublisherSerializer

from ..models import StoryArc


class StoryArcsListSerializer(serializers.ModelSerializer):
    image = serializers.ReadOnlyField(source="square_medium")
    publisher = NestedPublisherSerializer(read_only=True)
    issues_count = serializers.ReadOnlyField()
    volumes_count = serializers.ReadOnlyField()

    class Meta:
        model = StoryArc
        fields = ["slug", "image", "publisher", "name", "short_description", "issues_count", "volumes_count"]


class StartedStoryArcSerializer(serializers.ModelSerializer):
    image = serializers.ReadOnlyField(source="square_medium")
    max_finished_date = serializers.ReadOnlyField()
    finished_count = serializers.ReadOnlyField()
    issue_count = serializers.ReadOnlyField()

    class Meta:
        model = StoryArc
        fields = ["slug", "display_name", "image", "max_finished_date", "finished_count", "issue_count"]
