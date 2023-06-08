from rest_framework.viewsets import ReadOnlyModelViewSet
from utils.api.viewset_actions_mixins import CountActionMixin
from utils.api.viewset_queryset_mixins import (
    IssuesCountQuerySetMixin,
    OnlyWithIssuesQuerySetMixin,
    VolumesCountQuerySetMixin,
)

from ..models import Publisher


class PublishersViewSet(
    CountActionMixin,
    OnlyWithIssuesQuerySetMixin,
    IssuesCountQuerySetMixin,
    VolumesCountQuerySetMixin,
    ReadOnlyModelViewSet,
):
    volumes_lookup = "volumes"
    issues_lookup = "volumes__issues"

    queryset = Publisher.objects.was_matched()
