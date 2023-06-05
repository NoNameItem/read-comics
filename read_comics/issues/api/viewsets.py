from rest_framework.viewsets import ReadOnlyModelViewSet

from read_comics.utils.api.viewset_mixins import CountModelMixin

from ..models import Issue


class IssueViewSet(CountModelMixin, ReadOnlyModelViewSet):
    queryset = Issue.objects.was_matched().select_related("volume", "volume__publisher")
