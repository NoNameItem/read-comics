from django.db.models import Manager, QuerySet
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_extensions.mixins import DetailSerializerMixin
from utils.api.filters import UniqueOrderingFilter
from utils.api.viewset_actions_mixins import CountActionMixin, TechnicalInfoActionMixin
from utils.api.viewset_queryset_mixins import (
    IssuesCountQuerySetMixin,
    ListOnlyQuerySetMixin,
    OnlyWithIssuesQuerySetMixin,
    VolumesCountQuerySetMixin,
)

from ..models import Location
from .serializers import ConceptTechnicalInfoSerializer, LocationDetailSerializer, LocationsListSerializer


class LocationViewSet(
    DetailSerializerMixin,
    TechnicalInfoActionMixin,
    CountActionMixin,
    OnlyWithIssuesQuerySetMixin,
    IssuesCountQuerySetMixin,
    VolumesCountQuerySetMixin,
    ListOnlyQuerySetMixin,
    ReadOnlyModelViewSet,
):
    list_only = ["slug", "thumb_url", "name", "short_description"]

    serializer_class = LocationsListSerializer
    serializer_detail_class = LocationDetailSerializer
    serializer_tech_info_class = ConceptTechnicalInfoSerializer

    filter_backends = [UniqueOrderingFilter]
    ordering_fields = ["name", "issues_count", "volumes_count"]
    ordering = ["name"]

    lookup_field = "slug"
    lookup_url_kwarg = "slug"

    @property
    def queryset(self) -> QuerySet | Manager | None:
        return Location.objects.was_matched()

    @queryset.setter
    def queryset(self, _value) -> None:
        return
