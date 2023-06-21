from rest_framework import serializers

from read_comics.issues.models import Issue
from read_comics.publishers.api.serializers import NestedPublisherSerializer
from read_comics.volumes.api.serializers import NestedVolumeSerializer


class IssuesListSerializer(serializers.ModelSerializer):
    image = serializers.ReadOnlyField(source="square_medium")
    publisher = NestedPublisherSerializer(read_only=True, source="volume.publisher")
    name = serializers.ReadOnlyField(source="display_name")
    volume = NestedVolumeSerializer(read_only=True)
    is_finished = serializers.SerializerMethodField()

    def get_is_finished(self, obj: Issue):
        if obj.finished_flg is None:
            return None
        return obj.finished_flg == 1

    class Meta:
        model = Issue
        fields = ["slug", "image", "publisher", "name", "short_description", "cover_date", "volume", "is_finished"]


class IssueDetailSerializer(serializers.ModelSerializer):
    image = serializers.ReadOnlyField(source="full_size_url")
    square_image = serializers.ReadOnlyField(source="square_medium")
    publisher = NestedPublisherSerializer(read_only=True, source="volume.publisher")
    volume = NestedVolumeSerializer(read_only=True)
    is_finished = serializers.SerializerMethodField()
    prev_issue_slug = serializers.SerializerMethodField()
    next_issue_slug = serializers.SerializerMethodField()
    number_in_sublist = serializers.SerializerMethodField()
    total_in_sublist = serializers.SerializerMethodField()

    def get_is_finished(self, obj: Issue):
        if obj.finished_flg is None:
            return None
        return obj.finished_flg == 1

    def get_prev_issue_slug(self, _obj: Issue) -> str | None:
        return self.context.get("prev_issue_slug")

    def get_next_issue_slug(self, _obj: Issue) -> str | None:
        return self.context.get("next_issue_slug")

    def get_number_in_sublist(self, _obj: Issue) -> int:
        return self.context["number_in_sublist"]

    def get_total_in_sublist(self, _obj: Issue) -> int:
        return self.context["total_in_sublist"]

    class Meta:
        model = Issue
        fields = [
            "slug",
            "image",
            "square_image",
            "publisher",
            "volume",
            "number",
            "volume_last_number",
            "name",
            "cover_date",
            "store_date",
            "short_description",
            "description",
            "comicvine_url",
            "download_link",
            "download_size",
            "is_finished",
            "prev_issue_slug",
            "next_issue_slug",
            "number_in_sublist",
            "total_in_sublist",
        ]


class IssueTechnicalInfoSerializer(serializers.ModelSerializer):
    comicvine_status = serializers.ReadOnlyField(source="get_comicvine_status_display")

    class Meta:
        model = Issue
        fields = ["id", "comicvine_id", "comicvine_status", "comicvine_last_match", "created_dt", "modified_dt"]
