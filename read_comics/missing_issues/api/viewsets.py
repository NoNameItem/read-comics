from rest_framework.viewsets import ReadOnlyModelViewSet
from utils.api.viewset_mixins import CountModelMixin

from ..models import MissingIssue


class MissingIssueViewSet(CountModelMixin, ReadOnlyModelViewSet):
    queryset = MissingIssue.objects.filter(skip=False)
