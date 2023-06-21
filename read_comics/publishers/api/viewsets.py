from django.db.models import Manager, QuerySet
from rest_framework.viewsets import ReadOnlyModelViewSet
from utils.api.filters import UniqueOrderingFilter
from utils.api.viewset_actions_mixins import CountActionMixin
from utils.api.viewset_queryset_mixins import (
    IssuesCountQuerySetMixin,
    ListOnlyQuerySetMixin,
    OnlyWithIssuesQuerySetMixin,
    VolumesCountQuerySetMixin,
)

from ..models import Publisher
from .serializers import PublishersListSerializer


class PublishersViewSet(
    CountActionMixin,
    OnlyWithIssuesQuerySetMixin,
    IssuesCountQuerySetMixin,
    VolumesCountQuerySetMixin,
    ListOnlyQuerySetMixin,
    ReadOnlyModelViewSet,
):
    volumes_lookup = "volumes"
    issues_lookup = "volumes__issues"

    list_only = ["slug", "thumb_url", "name", "short_description"]

    serializer_class = PublishersListSerializer

    filter_backends = [UniqueOrderingFilter]
    ordering_fields = ["name", "issues_count", "volumes_count"]
    ordering = ["name"]

    @property
    def queryset(self) -> QuerySet | Manager | None:
        return Publisher.objects.was_matched()

    @queryset.setter
    def queryset(self, value) -> None:
        return
