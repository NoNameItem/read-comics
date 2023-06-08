from rest_framework.viewsets import ReadOnlyModelViewSet

from read_comics.utils.api.viewset_actions_mixins import CountActionMixin

from ..models import Issue


class IssueViewSet(CountActionMixin, ReadOnlyModelViewSet):
    queryset = Issue.objects.was_matched().select_related("volume", "volume__publisher")
