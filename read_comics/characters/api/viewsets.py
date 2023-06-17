from django.db.models import Manager, QuerySet
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_extensions.mixins import DetailSerializerMixin
from utils.api.filters import UniqueOrderingFilter
from utils.api.viewset_queryset_mixins import (
    IssuesCountQuerySetMixin,
    ListOnlyQuerySetMixin,
    OnlyWithIssuesQuerySetMixin,
    VolumesCountQuerySetMixin,
)

from read_comics.utils.api.viewset_actions_mixins import CountActionMixin, TechnicalInfoActionMixin

from ..models import Character
from .serializers import CharacterDetailSerializer, CharactersListSerializer, CharacterTechnicalInfoSerializer


class CharacterViewSet(
    DetailSerializerMixin,
    TechnicalInfoActionMixin,
    CountActionMixin,
    OnlyWithIssuesQuerySetMixin,
    IssuesCountQuerySetMixin,
    VolumesCountQuerySetMixin,
    ListOnlyQuerySetMixin,
    ReadOnlyModelViewSet,
):
    list_only = [
        "slug",
        "thumb_url",
        "name",
        "publisher__thumb_url",
        "publisher__name",
        "publisher__slug",
        "short_description",
    ]

    serializer_class = CharactersListSerializer
    serializer_detail_class = CharacterDetailSerializer
    serializer_tech_info_class = CharacterTechnicalInfoSerializer

    filter_backends = [UniqueOrderingFilter]
    ordering_fields = ["name", "issues_count", "volumes_count"]
    ordering = ["name"]
    lookup_field = "slug"
    lookup_url_kwarg = "slug"

    @property
    def queryset(self) -> QuerySet | Manager | None:
        return Character.objects.was_matched().select_related("publisher")

    @queryset.setter
    def queryset(self, _value) -> None:
        return
