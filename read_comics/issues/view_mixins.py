from django.db.models import Sum
from utils.utils import get_first_page


class IssuesViewMixin:
    def get_context_data(self, **kwargs):
        context = super(IssuesViewMixin, self).get_context_data(**kwargs)

        issues_info = {
            "count": self.sublist_querysets.get_issues_queryset(self.object).count(),
            "size": self.sublist_querysets.get_issues_queryset(self.object).aggregate(v=Sum('size'))['v'],
        }

        if self.request.user.is_authenticated:
            issues_info['finished_issues_count'] = self.sublist_querysets.get_issues_queryset(
                self.object, self.request.user
            ).exclude(finished_flg=0).count()
            try:
                issues_info['finished_percent'] = issues_info['finished_issues_count'] / issues_info['count'] * 100
            except ZeroDivisionError:
                issues_info['finished_percent'] = 100

        issues_info.update(
            get_first_page(self.sublist_querysets.get_issues_queryset(self.object, self.request.user))
        )
        context["issues_info"] = issues_info

        return context
