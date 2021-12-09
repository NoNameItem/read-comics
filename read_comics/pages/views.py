from typing import Any, Dict

from django.views.generic import TemplateView
from utils.comicvine_stats import get_matched_stats

from read_comics.missing_issues.models import MissingIssue


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(HomeView, self).get_context_data(**kwargs)
        context['matched_stats'] = get_matched_stats()
        context['missing_issues_count'] = MissingIssue.objects.all().count()
        return context


home_view = HomeView.as_view()
