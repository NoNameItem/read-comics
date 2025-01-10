from typing import Any, Dict

from django.db.models import Count, DateTimeField, Q
from django.db.models.functions import Trunc
from django.views.generic import DayArchiveView, TemplateView
from utils.comicvine_stats import get_matched_stats

from read_comics.issues.models import Issue
from read_comics.missing_issues.models import MissingIssue


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(HomeView, self).get_context_data(**kwargs)
        context["matched_stats"] = get_matched_stats()
        context["missing_issues_count"] = MissingIssue.objects.filter(skip=False).count()

        context["update_history"] = (
            Issue.objects.values(created_day=Trunc("created_dt", "day", output_field=DateTimeField()))
            .annotate(cnt=Count("id"))
            .order_by("-created_day")
        )

        if self.request.user.is_authenticated:
            context["finished_issues_count"] = (
                Issue.objects.matched()
                .annotate(
                    finished_flg=Count("finished_users", distinct=True, filter=Q(finished_users=self.request.user))
                )
                .exclude(finished_flg=0)
                .count()
            )
            try:
                context["finished_percent"] = (
                    context["finished_issues_count"] / context["matched_stats"]["issues_count"] * 100
                )
            except ZeroDivisionError:
                context["finished_percent"] = 0
            context["started_and_not_finished_volumes"] = self.request.user.started_and_not_finished_volumes
            context["started_and_not_finished_story_arcs"] = self.request.user.started_and_not_finished_story_arcs

        return context


home_view = HomeView.as_view()


class NewIssuesView(DayArchiveView):
    queryset = Issue.objects.matched().select_related("volume", "volume__publisher")
    ordering = ("volume__publisher", "volume", "numerical_number", "number")
    date_field = "created_dt"
    allow_future = True
    template_name = "pages/new_issues.html"
    context_object_name = "new_issues"
    month_format = "%m"


new_issues_view = NewIssuesView.as_view()
