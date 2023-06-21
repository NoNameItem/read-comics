import typing

from django.db.models import BooleanField, Case, Count, DateTimeField, F, IntegerField, Max, Q, QuerySet, Value, When
from rest_framework.viewsets import GenericViewSet

if typing.TYPE_CHECKING:
    _ViewSet = GenericViewSet
else:
    _ViewSet = object


class OnlyWithIssuesQuerySetMixin(_ViewSet):
    allways_show_all = False

    def get_queryset(self):
        qs = super().get_queryset()
        show_all = self.request.query_params.get("show-all", "no")
        if not self.allways_show_all and show_all != "yes" and not self.detail:
            return qs.filter(issues_count__gt=0)
        return qs


class ListOnlyQuerySetMixin(_ViewSet):
    list_only: list[str] = []

    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()
        if not self.detail and len(self.list_only) > 0:
            return qs.only(*self.list_only)
        return qs


class IssuesCountQuerySetMixin(_ViewSet):
    issues_lookup = "issues"

    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()
        if not self.detail:
            return qs.annotate(issues_count=Count(self.issues_lookup, distinct=True))
        return qs


class VolumesCountQuerySetMixin(_ViewSet):
    volumes_lookup = "issues__volume"

    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()
        if not self.detail:
            return qs.annotate(volumes_count=Count(self.volumes_lookup, distinct=True))
        return qs


if typing.TYPE_CHECKING:

    class _IssueCountViewSet(IssuesCountQuerySetMixin, GenericViewSet):
        pass

else:
    _IssueCountViewSet = object


class FinishedQuerySetMixin(_IssueCountViewSet):
    def get_queryset(self) -> QuerySet:
        user = self.request.user
        qs = super().get_queryset()
        if self.detail:
            return qs
        if user.is_authenticated:
            return qs.annotate(
                finished_count=Count(self.issues_lookup, filter=Q(issues__finished_users=user)),
                max_finished_date=Max(
                    f"{self.issues_lookup}__finished__finish_date", filter=Q(issues__finished__user=user)
                ),
            ).annotate(
                is_started=Case(When(finished_count__gte=1, then=Value(True)), default=False),
                is_finished=Case(When(finished_count=F("issues_count"), then=Value(True)), default=False),
            )
        return qs.annotate(
            finished_count=Value(None, output_field=IntegerField()),
            max_finished_date=Value(None, output_field=DateTimeField()),
            is_started=Value(None, output_field=BooleanField()),
            is_finished=Value(None, output_field=BooleanField()),
        )


if typing.TYPE_CHECKING:

    class _FinishedQuerySetViewSet(FinishedQuerySetMixin, GenericViewSet):
        pass

else:
    _FinishedQuerySetViewSet = object


class HideFinishedQuerySetMixin(_FinishedQuerySetViewSet):
    def get_queryset(self) -> QuerySet:
        q = super().get_queryset()
        if self.action == "list" and self.request.GET.get("hide-finished", "yes") == "yes":
            return q.filter(Q(is_finished=False) | Q(is_finished__isnull=True))
        return q
