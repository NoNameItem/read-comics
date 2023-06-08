from rest_framework.viewsets import ReadOnlyModelViewSet
from utils.api.viewset_actions_mixins import CountActionMixin

from ..models import MissingIssue


class MissingIssueViewSet(CountActionMixin, ReadOnlyModelViewSet):
    queryset = MissingIssue.objects.filter(skip=False)
