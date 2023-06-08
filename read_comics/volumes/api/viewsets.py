from rest_framework.viewsets import ReadOnlyModelViewSet
from utils.api.viewset_actions_mixins import CountActionMixin, StartedActionMixin
from utils.api.viewset_queryset_mixins import (
    FinishedQuerySetMixin,
    IssuesCountQuerySetMixin,
    OnlyWithIssuesQuerySetMixin,
)

from ..models import Volume
from .serializers import StartedVolumeSerializer


class VolumesViewSet(
    StartedActionMixin,
    CountActionMixin,
    FinishedQuerySetMixin,
    OnlyWithIssuesQuerySetMixin,
    IssuesCountQuerySetMixin,
    ReadOnlyModelViewSet,
):
    queryset = Volume.objects.was_matched().select_related("publisher")

    started_serializer = StartedVolumeSerializer
