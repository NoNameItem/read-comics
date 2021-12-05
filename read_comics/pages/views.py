from typing import Any, Dict

from django.views.generic import TemplateView
from utils.comicvine_stats import get_matched_stats


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(HomeView, self).get_context_data(**kwargs)
        context['matched_stats'] = get_matched_stats()
        return context


home_view = HomeView.as_view()
