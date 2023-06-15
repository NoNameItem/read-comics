from rest_framework.viewsets import ReadOnlyModelViewSet
from utils.api.filters import UniqueOrderingFilter
from utils.api.viewset_actions_mixins import CountActionMixin
from utils.api.viewset_queryset_mixins import (
    IssuesCountQuerySetMixin,
    OnlyWithIssuesQuerySetMixin,
    VolumesCountQuerySetMixin,
)

from ..models import Concept
from .serializers import ConceptsListSerializer


class ConceptViewSet(
    CountActionMixin,
    OnlyWithIssuesQuerySetMixin,
    IssuesCountQuerySetMixin,
    VolumesCountQuerySetMixin,
    ReadOnlyModelViewSet,
):
    queryset = Concept.objects.was_matched()
    serializer_class = ConceptsListSerializer

    filter_backends = [UniqueOrderingFilter]
    ordering_fields = ["name", "issues_count", "volumes_count"]
    ordering = ["name"]
