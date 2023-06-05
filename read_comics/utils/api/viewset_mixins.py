from typing import Protocol, TypeVar

from django.db.models import Model, QuerySet
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

_MT_co = TypeVar("_MT_co", bound=Model, covariant=True)


class UsesQuerySet(Protocol[_MT_co]):
    def get_queryset(self) -> QuerySet[_MT_co]:
        ...


class CountModelMixin:
    @action(detail=False)
    def count(self: UsesQuerySet, _request: Request) -> Response:
        return Response({"count": self.get_queryset().count()})
