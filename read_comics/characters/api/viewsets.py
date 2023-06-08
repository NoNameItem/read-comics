from rest_framework.viewsets import ReadOnlyModelViewSet
from utils.api.filters import UniqueOrderingFilter
from utils.api.viewset_queryset_mixins import (
    IssuesCountQuerySetMixin,
    ListOnlyQuerySetMixin,
    OnlyWithIssuesQuerySetMixin,
    VolumesCountQuerySetMixin,
)

from read_comics.utils.api.viewset_actions_mixins import CountActionMixin

from ..models import Character
from .serializers import CharactersListSerializer


class CharacterViewSet(
    CountActionMixin,
    OnlyWithIssuesQuerySetMixin,
    IssuesCountQuerySetMixin,
    VolumesCountQuerySetMixin,
    ListOnlyQuerySetMixin,
    ReadOnlyModelViewSet,
):
    queryset = (
        Character.objects.was_matched()
        .select_related("publisher")
        .only("slug", "thumb_url", "name", "publisher__thumb_url", "publisher__name", "short_description")
    )
    list_only = ["slug", "thumb_url", "name", "publisher__thumb_url", "publisher__name", "short_description"]

    serializer_class = CharactersListSerializer

    filter_backends = [UniqueOrderingFilter]
    ordering_fields = ["name", "issues_count", "volumes_count"]
    ordering = ["name"]
