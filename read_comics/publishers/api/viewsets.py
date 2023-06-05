from django.db.models import Count
from rest_framework.viewsets import ReadOnlyModelViewSet
from utils.api.viewset_mixins import CountModelMixin

from ..models import Publisher


class PublishersViewSet(CountModelMixin, ReadOnlyModelViewSet):
    queryset = (
        Publisher.objects.was_matched()
        .annotate(volume_count=Count("volumes", distinct=True))
        .annotate(issue_count=Count("volumes__issues", distinct=True))
    )
