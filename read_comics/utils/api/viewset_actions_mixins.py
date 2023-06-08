import typing

from django.core.exceptions import ImproperlyConfigured
from rest_framework import exceptions
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet
from utils.api.viewset_queryset_mixins import FinishedQuerySetMixin

from read_comics.users.models import User

if typing.TYPE_CHECKING:
    _ViewSet = GenericViewSet
else:
    _ViewSet = object

if typing.TYPE_CHECKING:

    class _FinishedQuerySetViewSet(FinishedQuerySetMixin, _ViewSet):
        pass

else:
    _FinishedQuerySetViewSet = object


class CountActionMixin(_ViewSet):
    @action(detail=False)
    def count(self, _request: Request) -> Response:
        return Response({"count": self.get_queryset().count()})


class StartedActionMixin(_FinishedQuerySetViewSet):
    started_serializer: type[Serializer]

    @action(detail=False, permission_classes=[IsAuthenticated])
    def started(self, request: Request, *args, **kwargs) -> Response:
        if self.started_serializer is None:
            raise ImproperlyConfigured("set started_serializer field")
        user = request.user
        if not isinstance(user, User):
            raise exceptions.NotAuthenticated
        qs = self.get_queryset()
        qs = qs.filter(is_started=True, is_finished=False).order_by("-max_finished_date")

        page = self.paginate_queryset(qs)
        serializer = self.started_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
