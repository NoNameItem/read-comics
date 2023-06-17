from django.db.models import Count, IntegerField, Manager, Q, QuerySet, Value
from rest_framework.viewsets import ReadOnlyModelViewSet
from utils.api.filters import UniqueOrderingFilter

from read_comics.utils.api.viewset_actions_mixins import CountActionMixin

from ..models import Issue
from .serializers import IssuesListSerializer


class IssueViewSet(CountActionMixin, ReadOnlyModelViewSet):
    serializer_class = IssuesListSerializer
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
    ordering = ["cover_date", "volume", "volume__start_year", "number"]

    @property
    def queryset(self) -> QuerySet | Manager | None:
        return Issue.objects.was_matched().select_related("volume", "volume__publisher")

    @queryset.setter
    def queryset(self, _value) -> None:
        return

    def get_queryset(self) -> QuerySet:
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
            q = q.annotate(finished_flg=Value(0, output_field=IntegerField()))

        # Hide finished
        if self.request.GET.get("hide-finished", "yes") == "yes":
            return q.filter(finished_flg=0)
        return q
