from django.db.models import Count
from rest_framework.viewsets import ReadOnlyModelViewSet

from read_comics.utils.api.viewset_mixins import CountModelMixin

from ..models import Character


class CharacterViewSet(CountModelMixin, ReadOnlyModelViewSet):
    queryset = (
        Character.objects.was_matched()
        .annotate(volume_count=Count("issues__volume", distinct=True))
        .annotate(issue_count=Count("issues", distinct=True))
        .select_related("publisher")
        .only("slug", "thumb_url", "name", "publisher__thumb_url", "publisher__name", "short_description")
    )
