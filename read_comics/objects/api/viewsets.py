from django.db.models import Count
from rest_framework.viewsets import ReadOnlyModelViewSet
from utils.api.viewset_mixins import CountModelMixin

from ..models import Object


class ObjectViewSet(CountModelMixin, ReadOnlyModelViewSet):
    queryset = (
        Object.objects.was_matched()
        .annotate(volume_count=Count("issues__volume", distinct=True))
        .annotate(issue_count=Count("issues", distinct=True))
    )
