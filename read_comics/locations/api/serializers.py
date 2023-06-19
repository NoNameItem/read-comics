from rest_framework import serializers

from ..models import Location


class LocationsListSerializer(serializers.ModelSerializer):
    image = serializers.ReadOnlyField(source="square_medium")
    issues_count = serializers.ReadOnlyField()
    volumes_count = serializers.ReadOnlyField()

    class Meta:
        model = Location
        fields = ["slug", "image", "name", "short_description", "issues_count", "volumes_count"]


class LocationDetailSerializer(serializers.ModelSerializer):
    image = serializers.ReadOnlyField(source="full_size_url")
    square_image = serializers.ReadOnlyField(source="square_medium")
    aliases = serializers.ReadOnlyField(source="get_aliases_list")
    first_issue_name = serializers.SerializerMethodField()
    first_issue_slug = serializers.SerializerMethodField()
    download_link = serializers.SerializerMethodField()

    @staticmethod
    def get_first_issue_name(obj: Location) -> str | None:
        return obj.first_issue.display_name if obj.first_issue else obj.first_issue_name

    @staticmethod
    def get_first_issue_slug(obj: Location) -> str | None:
        return obj.first_issue.slug if obj.first_issue else None

    def get_download_link(self, obj: Location) -> str:
        return self.context["request"].build_absolute_uri(obj.download_link)

    class Meta:
        model = Location
        fields = [
            "slug",
            "name",
            "image",
            "square_image",
            "aliases",
            "start_year",
            "first_issue_name",
            "first_issue_slug",
            "comicvine_url",
            "short_description",
            "description",
            "download_link",
            "download_size",
        ]


class ConceptTechnicalInfoSerializer(serializers.ModelSerializer):
    comicvine_status = serializers.ReadOnlyField(source="get_comicvine_status_display")

    class Meta:
        model = Location
        fields = ["id", "comicvine_id", "comicvine_status", "comicvine_last_match", "created_dt", "modified_dt"]
