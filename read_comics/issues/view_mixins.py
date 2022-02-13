from django.db.models import Count, F, Func, Q, Sum, TextField, Value
from django.db.models.functions import Concat
from utils.utils import get_first_page


class IssuesSublistQueryset:
    @staticmethod
    def _get_issues_sublist(obj):
        return obj.issues.filter(comicvine_status="MATCHED")

    @staticmethod
    def _order_issues(q):
        return q.order_by("cover_date", "volume__name", "volume__start_year", "numerical_number", "number")

    @staticmethod
    def _annotate_issues(q, obj):
        return q.annotate(
            parent_slug=Value(obj.slug),
            badge_name=Concat(
                F("volume__name"), Value(" ("), F("volume__start_year"), Value(") #"), F("number"), Value(" "),
                F("name"),
                output_field=TextField()
            ),
            desc=F("cover_date")
        )

    @staticmethod
    def _break_issues(q):
        return q.annotate(
            group_breaker=Func(F("cover_date"), Value("Month YYYY"), function="to_char", output_field=TextField())
        )

    @staticmethod
    def _annotate_issues_as_finished(q, user):
        if user and user.is_authenticated:
            return q.annotate(finished_flg=Count("finished_users", distinct=True, filter=Q(finished_users=user)))
        return q

    def get_issues_queryset(self, obj, user=None):
        return self._annotate_issues_as_finished(
            self._break_issues(
                self._annotate_issues(
                    self._order_issues(
                        self._get_issues_sublist(obj)
                    ),
                    obj
                )
            ),
            user
        )


class IssuesViewMixin:
    sublist_querysets: IssuesSublistQueryset

    def get_context_data(self, **kwargs: object) -> dict:
        context = super(IssuesViewMixin, self).get_context_data(**kwargs)

        issues_info = {
            "count": self.sublist_querysets.get_issues_queryset(self.object).count(),
            "size": self.sublist_querysets.get_issues_queryset(self.object).aggregate(v=Sum("size"))["v"],
        }

        if self.request.user.is_authenticated:
            issues_info["finished_issues_count"] = self.sublist_querysets.get_issues_queryset(
                self.object, self.request.user
            ).exclude(finished_flg=0).count()
            try:
                issues_info["finished_percent"] = issues_info["finished_issues_count"] / issues_info["count"] * 100
            except ZeroDivisionError:
                issues_info["finished_percent"] = 100

        issues_info.update(
            get_first_page(self.sublist_querysets.get_issues_queryset(self.object, self.request.user))
        )
        context["issues_info"] = issues_info

        return context
