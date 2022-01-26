import datetime
from typing import Any, Dict

from django.db.models import Count, DateTimeField, Max, Q
from django.db.models.functions import Trunc
from django.views.generic import TemplateView
from utils.comicvine_stats import get_matched_stats

from read_comics.issues.models import Issue
from read_comics.missing_issues.models import MissingIssue


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(HomeView, self).get_context_data(**kwargs)
        context['matched_stats'] = get_matched_stats()
        context['missing_issues_count'] = MissingIssue.objects.all().count()

        last_update_day = Issue.objects.aggregate(
            max_day=Max(Trunc('created_dt', 'day', output_field=DateTimeField()))
        )['max_day']
        new_issues = Issue.objects.matched().filter(
            created_dt__gte=last_update_day, created_dt__lt=last_update_day + datetime.timedelta(days=1)
        ).order_by(
            'volume__publisher', 'volume', 'numerical_number', 'number'
        ).select_related(
            'volume', 'volume__publisher'
        )
        context['last_update_day'] = last_update_day
        context['new_issues'] = new_issues
        context['new_issues_count'] = new_issues.count()

        if self.request.user.is_authenticated:
            context['finished_issues_count'] = Issue.objects.matched().annotate(
                finished_flg=Count('finished_users', distinct=True, filter=Q(finished_users=self.request.user))
            ).exclude(finished_flg=0).count()
            context['finished_percent'] = \
                context['finished_issues_count'] / context['matched_stats']['issues_count'] * 100

        return context


home_view = HomeView.as_view()
