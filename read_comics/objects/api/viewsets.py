from rest_framework.viewsets import ReadOnlyModelViewSet
from utils.api.viewset_actions_mixins import CountActionMixin
from utils.api.viewset_queryset_mixins import (
    IssuesCountQuerySetMixin,
    OnlyWithIssuesQuerySetMixin,
    VolumesCountQuerySetMixin,
)

from ..models import Object


class ObjectViewSet(
    CountActionMixin,
    OnlyWithIssuesQuerySetMixin,
    IssuesCountQuerySetMixin,
    VolumesCountQuerySetMixin,
    ReadOnlyModelViewSet,
):
    queryset = Object.objects.was_matched()
