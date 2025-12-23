# Docs: [[docs/backend/volumes/api/viewsets.md]]
from django.db.models import Manager, QuerySet
from rest_framework.viewsets import ReadOnlyModelViewSet
from read_comics.utils.api.filters import UniqueOrderingFilter
from read_comics.utils.api.viewset_actions_mixins import CountActionMixin, StartedActionMixin
from read_comics.utils.api.viewset_queryset_mixins import (
    FinishedQuerySetMixin,
    HideFinishedQuerySetMixin,
    IssuesCountQuerySetMixin,
    ListOnlyQuerySetMixin,
)

from ..models import Volume
from .serializers import StartedVolumeSerializer, VolumesListSerializer


class VolumesViewSet(
    StartedActionMixin,
    CountActionMixin,
    HideFinishedQuerySetMixin,
    FinishedQuerySetMixin,
    IssuesCountQuerySetMixin,
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
    serializer_class = VolumesListSerializer
    started_serializer = StartedVolumeSerializer

    filter_backends = [UniqueOrderingFilter]
    ordering_fields = ["name", "issues_count", "start_year"]
    ordering = ["start_year"]

    @property
    def queryset(self) -> QuerySet | Manager | None:
        return Volume.objects.was_matched().select_related("publisher")

    @queryset.setter
    def queryset(self, _value) -> None:
        return
