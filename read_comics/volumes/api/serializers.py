from rest_framework import serializers

from read_comics.publishers.api.serializers import NestedPublisherSerializer

from ..models import Volume


class NestedVolumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volume
        fields = ["slug", "display_name", "start_year", "name"]


class VolumesListSerializer(serializers.ModelSerializer):
    image = serializers.ReadOnlyField(source="square_medium")
    publisher = NestedPublisherSerializer(read_only=True)
    issues_count = serializers.ReadOnlyField()
    finished_count = serializers.ReadOnlyField()
    is_finished = serializers.ReadOnlyField()

    class Meta:
        model = Volume
        fields = [
            "slug",
            "image",
            "publisher",
            "name",
            "short_description",
            "issues_count",
            "finished_count",
            "is_finished",
            "start_year",
        ]


class StartedVolumeSerializer(serializers.ModelSerializer):
    image = serializers.ReadOnlyField(source="square_medium")
    max_finished_date = serializers.ReadOnlyField()
    finished_count = serializers.ReadOnlyField()
    issues_count = serializers.ReadOnlyField()

    class Meta:
        model = Volume
        fields = ["slug", "display_name", "image", "max_finished_date", "finished_count", "issues_count"]
