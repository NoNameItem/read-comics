from rest_framework.viewsets import ReadOnlyModelViewSet
from utils.api.filters import UniqueOrderingFilter
from utils.api.viewset_actions_mixins import CountActionMixin
from utils.api.viewset_queryset_mixins import (
    IssuesCountQuerySetMixin,
    OnlyWithIssuesQuerySetMixin,
    VolumesCountQuerySetMixin,
)

from ..models import Location
from .serializers import LocationsListSerializer


class LocationViewSet(
    CountActionMixin,
    OnlyWithIssuesQuerySetMixin,
    IssuesCountQuerySetMixin,
    VolumesCountQuerySetMixin,
    ReadOnlyModelViewSet,
):
    queryset = Location.objects.was_matched()

    serializer_class = LocationsListSerializer

    filter_backends = [UniqueOrderingFilter]
    ordering_fields = ["name", "issues_count", "volumes_count"]
    ordering = ["name"]
