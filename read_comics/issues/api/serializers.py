from rest_framework import serializers

from read_comics.issues.models import Issue
from read_comics.publishers.api.serializers import NestedPublisherSerializer
from read_comics.volumes.api.serializers import NestedVolumeSerializer


class IssuesListSerializer(serializers.ModelSerializer):
    image = serializers.ReadOnlyField(source="square_medium")
    publisher = NestedPublisherSerializer(read_only=True, source="volume.publisher")
    name = serializers.ReadOnlyField(source="display_name")
    volume = NestedVolumeSerializer(read_only=True)
    finished_flg = serializers.ReadOnlyField()

    class Meta:
        model = Issue
        fields = ["slug", "image", "publisher", "name", "short_description", "cover_date", "volume", "finished_flg"]
