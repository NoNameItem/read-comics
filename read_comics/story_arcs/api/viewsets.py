from rest_framework.viewsets import ReadOnlyModelViewSet
from utils.api.viewset_actions_mixins import CountActionMixin, StartedActionMixin
from utils.api.viewset_queryset_mixins import (
    FinishedQuerySetMixin,
    IssuesCountQuerySetMixin,
    OnlyWithIssuesQuerySetMixin,
    VolumesCountQuerySetMixin,
)

from ..models import StoryArc
from .serializers import StartedStoryArcSerializer


class StoryArcsViewSet(
    StartedActionMixin,
    CountActionMixin,
    FinishedQuerySetMixin,
    OnlyWithIssuesQuerySetMixin,
    IssuesCountQuerySetMixin,
    VolumesCountQuerySetMixin,
    ReadOnlyModelViewSet,
):
    queryset = StoryArc.objects.was_matched().select_related("publisher")
    started_serializer = StartedStoryArcSerializer
