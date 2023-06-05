from django.db.models import Count
from rest_framework import exceptions
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from utils.api.viewset_mixins import CountModelMixin

from read_comics.users.models import User

from ..models import StoryArc
from .serializers import StartedStoryArcSerializer


class StoryArcsViewSet(CountModelMixin, ReadOnlyModelViewSet):
    queryset = (
        StoryArc.objects.was_matched()
        .annotate(volume_count=Count("issues__volume", distinct=True))
        .annotate(issue_count=Count("issues", distinct=True))
        .select_related("publisher")
    )

    @action(detail=False, permission_classes=[IsAuthenticated])
    def started(self, request: Request, *args, **kwargs) -> Response:
        user = request.user
        if not isinstance(user, User):
            raise exceptions.NotAuthenticated
        queryset = user.started_and_not_finished_story_arcs

        page = self.paginate_queryset(queryset)
        serializer = StartedStoryArcSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)
