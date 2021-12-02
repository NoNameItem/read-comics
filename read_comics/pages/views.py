from typing import Any, Dict

from django.views.generic import TemplateView

from read_comics.issues.models import Issue
from read_comics.publishers.models import Publisher
from read_comics.story_arcs.models import StoryArc
from read_comics.volumes.models import Volume


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(HomeView, self).get_context_data(**kwargs)
        context['issues_count'] = Issue.objects.matched().count()
        context['publishers_count'] = Publisher.objects.matched().count()
        context['story_arcs_count'] = StoryArc.objects.matched().count()
        context['volumes_count'] = Volume.objects.matched().count()
        return context


home_view = HomeView.as_view()
