from utils import logging
from utils.view_mixins import BreadcrumbMixin, ElidedPagesPaginatorMixin
from watson.views import SearchApiView
from watson.views import SearchView as BaseSearchView

from read_comics.characters.models import Character
from read_comics.concepts.models import Concept
from read_comics.issues.models import Issue
from read_comics.locations.models import Location
from read_comics.objects.models import Object
from read_comics.people.models import Person
from read_comics.publishers.models import Publisher
from read_comics.story_arcs.models import StoryArc
from read_comics.teams.models import Team
from read_comics.volumes.models import Volume

logger = logging.getLogger(__name__)


class RestrictModelMixin:
    MODELS = {
        'all': (),
        'characters': (Character, ),
        'concepts': (Concept, ),
        'issues': (Issue, ),
        'locations': (Location, ),
        'objects': (Object, ),
        'people': (Person, ),
        'publishers': (Publisher, ),
        'story_arcs': (StoryArc, ),
        'teams': (Team, ),
        'volumes': (Volume, )
    }

    MODEL_PARAM = 'category'

    def __init__(self, **kwargs):
        super(RestrictModelMixin, self).__init__(**kwargs)
        self.category = None

    def get_models(self):
        self.category = self.request.GET.get(self.MODEL_PARAM, 'all').strip()
        model = self.MODELS[self.category]
        return model


@logging.methods_logged(logger, ['get', ])
class SearchView(ElidedPagesPaginatorMixin, RestrictModelMixin, BreadcrumbMixin, BaseSearchView):
    template_name = "search/search.html"
    paginate_by = 50
    breadcrumb = [{'url': '#', 'text': 'Search'}]

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['category'] = self.category
        context['total_results'] = context['paginator'].count
        return context


search_view = SearchView.as_view()


@logging.methods_logged(logger, ['get', ])
class AjaxSearchView(RestrictModelMixin, SearchApiView):
    def get_queryset(self):
        q = super(AjaxSearchView, self).get_queryset()[:10]
        return q


ajax_search_view = AjaxSearchView.as_view()
