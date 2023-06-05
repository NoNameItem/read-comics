from rest_framework import serializers

from ..models import Volume


class StartedVolumeSerializer(serializers.ModelSerializer):
    image = serializers.ReadOnlyField(source="square_medium")
    max_finished_date = serializers.ReadOnlyField()
    finished_count = serializers.ReadOnlyField()
    issue_count = serializers.ReadOnlyField()

    class Meta:
        model = Volume
        fields = ["slug", "display_name", "image", "max_finished_date", "finished_count", "issue_count"]
