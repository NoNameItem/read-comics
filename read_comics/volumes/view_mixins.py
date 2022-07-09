from django.db.models import Case, Count, F, Q, TextField, Value, When
from django.db.models.functions import Concat
from utils.utils import get_first_page

from .models import Volume


class VolumesSublistQueryset:
    @staticmethod
    def _get_volumes_sublist(obj):
        return Volume.objects.filter(
            issues__in=obj.issues.all(),
            comicvine_status="MATCHED"
        )

    @staticmethod
    def _order_volumes(q):
        return q.order_by("start_year", "name", "id")

    @staticmethod
    def _annotate_volumes(q):
        return q.annotate(
            issues_count=Count("issues", distinct=True),
            badge_name=Concat(F("name"), Value(" ("), F("start_year"), Value(")"),
                              output_field=TextField()),
            desc=Concat(F("issues_count"), Value(" issue(s)"), output_field=TextField())
        )

    @staticmethod
    def _break_volumes(q):
        return q.annotate(
            group_breaker=F("start_year")
        )

    @staticmethod
    def _annotate_volumes_as_finished(q, user):
        if user and user.is_authenticated:
            return q.annotate(
                finished_count=Count("issues", filter=Q(issues__finished_users=user))
            ).annotate(
                finished_flg=Case(When(finished_count=F("issues_count"), then=1), default=0)
            )
        return q

    def get_volumes_queryset(self, obj, user=None):
        return self._annotate_volumes_as_finished(
            self._break_volumes(
                self._annotate_volumes(
                    self._order_volumes(
                        self._get_volumes_sublist(obj)
                    )
                )
            ),
            user
        )


class VolumesViewMixin:
    sublist_querysets: VolumesSublistQueryset

    def get_context_data(self, **kwargs: object) -> dict:
        context = super(VolumesViewMixin, self).get_context_data(**kwargs)

        volumes_info = {
            "count": self.sublist_querysets.get_volumes_queryset(self.object).count(),
        }

        volumes_info.update(
            get_first_page(self.sublist_querysets.get_volumes_queryset(self.object, self.request.user))
        )
        context["volumes_info"] = volumes_info

        return context
