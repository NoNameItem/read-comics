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


class CharacterDetailSerializer(serializers.ModelSerializer):
    image = serializers.ReadOnlyField(source="full_size_url")
    square_image = serializers.ReadOnlyField(source="square_medium")
    publisher = NestedPublisherSerializer(read_only=True)
    aliases = serializers.ReadOnlyField(source="get_aliases_list")
    gender = serializers.ReadOnlyField(source="get_gender_display")
    powers: serializers.StringRelatedField = serializers.StringRelatedField(
        source="powers.all", many=True, read_only=True
    )
    first_issue_name = serializers.SerializerMethodField()
    first_issue_slug = serializers.SerializerMethodField()
    download_link = serializers.SerializerMethodField()

    @staticmethod
    def get_first_issue_name(obj: Character) -> str | None:
        return obj.first_issue.display_name if obj.first_issue else obj.first_issue_name

    @staticmethod
    def get_first_issue_slug(obj: Character) -> str | None:
        return obj.first_issue.slug if obj.first_issue else None

    def get_download_link(self, obj: Character) -> str:
        return self.context["request"].build_absolute_uri(obj.download_link)

    class Meta:
        model = Character
        fields = [
            "slug",
            "name",
            "real_name",
            "image",
            "square_image",
            "publisher",
            "aliases",
            "birth",
            "gender",
            "powers",
            "first_issue_name",
            "first_issue_slug",
            "comicvine_url",
            "description",
            "download_link",
            "download_size",
        ]


class CharacterTechnicalInfoSerializer(serializers.ModelSerializer):
    comicvine_status = serializers.ReadOnlyField(source="get_comicvine_status_display")

    class Meta:
        model = Character
        fields = ["id", "comicvine_id", "comicvine_status", "comicvine_last_match", "created_dt", "modified_dt"]
