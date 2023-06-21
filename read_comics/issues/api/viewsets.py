from collections.abc import Sequence
from typing import Any

from django.db.models import Count, IntegerField, Manager, Q, QuerySet, Value
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_extensions.mixins import DetailSerializerMixin
from utils.api.filters import UniqueOrderingFilter

from read_comics.utils.api.viewset_actions_mixins import CountActionMixin, TechnicalInfoActionMixin

from ..models import Issue
from .serializers import IssueDetailSerializer, IssuesListSerializer, IssueTechnicalInfoSerializer


class IssueViewSet(DetailSerializerMixin, TechnicalInfoActionMixin, CountActionMixin, ReadOnlyModelViewSet):
    serializer_class = IssuesListSerializer
    serializer_detail_class = IssueDetailSerializer
    serializer_tech_info_class = IssueTechnicalInfoSerializer

    list_only = [
        "slug",
        "image_url",
        "thumb_url",
        "volume__publisher__name",
        "volume__publisher__slug",
        "volume__publisher__thumb_url",
        "volume_id",
        "volume__name",
        "volume__start_year",
        "volume__slug",
        "number",
        "name",
        "short_description",
        "cover_date",
    ]

    filter_backends = [UniqueOrderingFilter]
    ordering_fields = ["volume__name", "volume__start_year", "numerical_number", "number", "cover_date"]
    ordering = ["cover_date", "volume__name", "volume__start_year", "numerical_number", "number"]

    lookup_field = "slug"
    lookup_url_kwarg = "slug"

    @property
    def queryset(self) -> QuerySet | Manager | None:
        return Issue.objects.was_matched().select_related("volume", "volume__publisher")

    @queryset.setter
    def queryset(self, _value) -> None:
        return

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        q = super().get_queryset()

        # Restrict list fields
        if not self.detail and len(self.list_only) > 0:
            q = q.only(*self.list_only)

        # Add finished flag
        if self.request.user.is_authenticated:
            q = q.annotate(
                finished_flg=Count("finished_users", distinct=True, filter=Q(finished_users=self.request.user))
            )
        else:
            q = q.annotate(finished_flg=Value(None, output_field=IntegerField()))

        # Hide finished
        if self.action == "list" and self.request.GET.get("hide-finished", "yes") == "yes":
            return q.filter(Q(finished_flg=0) | Q(finished_flg__isnull=True))
        return q

    def get_orderings(self) -> Sequence[str]:
        ordering_filter_backend = self.filter_backends[0]()
        if isinstance(ordering_filter_backend, UniqueOrderingFilter):
            return ordering_filter_backend.get_ordering(request=self.request, queryset=self.get_queryset(), view=self)
        return []

    def get_serializer_context(self) -> dict[str, Any]:
        context = super().get_serializer_context()
        if self.action == "retrieve":
            instance = self.get_object()
            context["next_issue_slug"] = self.get_next_issue_slug(instance)
            context["prev_issue_slug"] = self.get_prev_issue_slug(instance)
            context["number_in_sublist"] = self.get_number_in_sublist(instance)
            context["total_in_sublist"] = self.get_queryset().count()
        return context

    @staticmethod
    def get_field(ordering: str) -> str:
        if ordering[0] == "-":
            return ordering[1:]
        return ordering

    @staticmethod
    def reverse_orderings(orderings: Sequence[str]) -> Sequence[str]:
        orderings_without_id = orderings[:-1]
        return [ordering[1:] if ordering[0] == "-" else f"-{ordering}" for ordering in orderings_without_id] + ["id"]

    @staticmethod
    def get_field_value(instance: Any, field: str) -> Any:
        value = instance
        attrs = field.split("__")
        for attr in attrs:
            value = getattr(value, attr)
        return value

    def get_prev_filter(self, ordering: str, instance: Any) -> Q | None:
        field = self.get_field(ordering)
        lookup = "gt" if ordering[0] == "-" else "lt"
        value = self.get_field_value(instance, field)
        if value is not None:
            q = Q(**{f"{field}__{lookup}": value})
            if ordering[0] == "-":
                return q | Q(**{f"{field}__isnull": True})
            return q
        if ordering[0] != "-":
            return Q(**{f"{field}__isnull": False})
        return None

    def get_equal_filter(self, ordering: str, instance: Any) -> Q:
        field = self.get_field(ordering)
        value = self.get_field_value(instance, field)
        return Q(**{field: value}) if value is not None else Q(**{f"{field}__isnull": True})

    def get_next_filter(self, ordering: str, instance: Any) -> Q | None:
        field = self.get_field(ordering)
        lookup = "lt" if ordering[0] == "-" else "gt"
        value = self.get_field_value(instance, field)
        if value is not None:
            q = Q(**{f"{field}__{lookup}": value})
            if ordering[0] == "-":
                return q
            return q | Q(**{f"{field}__isnull": True})
        if ordering[0] == "-":
            return Q(**{f"{field}__isnull": False})
        return None

    def get_prev_filters(self, orderings: Sequence[str], instance: Any) -> Q | None:
        equal_cumulative_filter: Q | None = None
        result: Q | None = None
        for ordering in orderings:
            prev_filter = self.get_prev_filter(ordering, instance)
            if prev_filter is not None:
                equal_prev_filter = equal_cumulative_filter & prev_filter if equal_cumulative_filter else prev_filter
                result = result | equal_prev_filter if result else equal_prev_filter
            equal_filter = self.get_equal_filter(ordering, instance)
            equal_cumulative_filter = (
                equal_cumulative_filter & equal_filter if equal_cumulative_filter else equal_filter
            )
        return result

    def get_next_filters(self, orderings: Sequence[str], instance: Any) -> Q | None:
        equal_cumulative_filter: Q | None = None
        result: Q | None = None
        for ordering in orderings:
            next_filter = self.get_next_filter(ordering, instance)
            if next_filter is not None:
                equal_next_filter = equal_cumulative_filter & next_filter if equal_cumulative_filter else next_filter
                result = result | equal_next_filter if result else equal_next_filter
            equal_filter = self.get_equal_filter(ordering, instance)
            equal_cumulative_filter = (
                equal_cumulative_filter & equal_filter if equal_cumulative_filter else equal_filter
            )
        return result

    def get_next_issue_slug(self, instance) -> str | None:
        orderings = self.get_orderings()
        next_issues = self.get_queryset().filter(self.get_next_filters(orderings, instance)).order_by(*orderings)
        return next_issues[0].slug if next_issues.count() > 0 else None

    def get_prev_issue_slug(self, instance) -> str | None:
        orderings = self.get_orderings()
        prev_issues = (
            self.get_queryset()
            .filter(self.get_prev_filters(orderings, instance))
            .order_by(*self.reverse_orderings(orderings))
        )
        return prev_issues[0].slug if prev_issues.count() > 0 else None

    def get_number_in_sublist(self, instance):
        orderings = self.get_orderings()
        return self.get_queryset().filter(self.get_prev_filters(orderings, instance)).count() + 1
