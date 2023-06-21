from django.db.models import Manager, QuerySet
from rest_framework.viewsets import ReadOnlyModelViewSet
from utils.api.filters import UniqueOrderingFilter
from utils.api.viewset_actions_mixins import CountActionMixin, StartedActionMixin
from utils.api.viewset_queryset_mixins import (
    FinishedQuerySetMixin,
    HideFinishedQuerySetMixin,
    IssuesCountQuerySetMixin,
    ListOnlyQuerySetMixin,
    VolumesCountQuerySetMixin,
)

from ..models import StoryArc
from .serializers import StartedStoryArcSerializer, StoryArcsListSerializer


class StoryArcsViewSet(
    StartedActionMixin,
    CountActionMixin,
    HideFinishedQuerySetMixin,
    FinishedQuerySetMixin,
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
    serializer_class = StoryArcsListSerializer
    started_serializer = StartedStoryArcSerializer

    filter_backends = [UniqueOrderingFilter]
    ordering_fields = ["name", "issues_count", "volumes_count"]
    ordering = ["name"]

    @property
    def queryset(self) -> QuerySet | Manager | None:
        return StoryArc.objects.was_matched().select_related("publisher")

    @queryset.setter
    def queryset(self, _value) -> None:
        return
