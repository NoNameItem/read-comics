from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_extensions.mixins import DetailSerializerMixin
from utils.api.filters import UniqueOrderingFilter
from utils.api.viewset_actions_mixins import CountActionMixin, TechnicalInfoActionMixin
from utils.api.viewset_queryset_mixins import (
    IssuesCountQuerySetMixin,
    OnlyWithIssuesQuerySetMixin,
    VolumesCountQuerySetMixin,
)

from ..models import Concept
from .serializers import ConceptDetailSerializer, ConceptsListSerializer, ConceptTechnicalInfoSerializer


class ConceptViewSet(
    DetailSerializerMixin,
    TechnicalInfoActionMixin,
    CountActionMixin,
    OnlyWithIssuesQuerySetMixin,
    IssuesCountQuerySetMixin,
    VolumesCountQuerySetMixin,
    ReadOnlyModelViewSet,
):
    queryset = Concept.objects.was_matched()
    serializer_class = ConceptsListSerializer
    serializer_detail_class = ConceptDetailSerializer
    serializer_tech_info_class = ConceptTechnicalInfoSerializer

    filter_backends = [UniqueOrderingFilter]
    ordering_fields = ["name", "issues_count", "volumes_count"]
    ordering = ["name"]

    lookup_field = "slug"
    lookup_url_kwarg = "slug"
