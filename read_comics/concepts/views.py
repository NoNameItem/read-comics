from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from issues.views import IssueDetailView
from utils import logging
from utils.utils import get_first_page
from utils.view_mixins import (
    ActiveMenuMixin,
    BreadcrumbMixin,
    ElidedPagesPaginatorMixin,
    OnlyWithIssuesMixin,
    OrderingMixin,
)
from utils.views import BaseSublistView
from zip_download.views import BaseZipDownloadView

from read_comics.missing_issues.views import BaseStartWatchView, BaseStopWatchView

from . import sublist_querysets
from .models import Concept

logger = logging.getLogger(__name__)


@logging.methods_logged(logger, ['get', ])
class ConceptsListView(ElidedPagesPaginatorMixin, ActiveMenuMixin, OnlyWithIssuesMixin, OrderingMixin, BreadcrumbMixin,
                       ListView):
    context_object_name = "concepts"
    template_name = "concepts/list.html"
    breadcrumb = [{'url': reverse_lazy("concepts:list"), 'text': 'Concepts'}]
    paginate_by = 48
    possible_order = ('issue_count', '-issue_count', 'volume_count', '-volume_count', 'name', '-name')
    default_ordering = 'name'
    queryset = Concept.objects.was_matched().annotate(
        volume_count=Count('issues__volume', distinct=True)
    ).annotate(
        issue_count=Count('issues', distinct=True)
    )
    active_menu_item = 'concepts'


concepts_list_view = ConceptsListView.as_view()


@logging.methods_logged(logger, ['get', ])
class ConceptDetailView(ActiveMenuMixin, BreadcrumbMixin, DetailView):
    model = Concept
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "concept"
    template_name = "concepts/detail.html"
    active_menu_item = 'concepts'

    def get_breadcrumb(self):
        concept = self.object
        return [
            {'url': reverse_lazy("concepts:list"), 'text': 'Concepts'},
            {'url': '#',
             'text': concept.name}
        ]

    def get_context_data(self, **kwargs):
        context = super(ConceptDetailView, self).get_context_data(**kwargs)
        concept = self.object

        context['issues_count'] = sublist_querysets.get_issues_queryset(concept).count()
        context['volumes_count'] = sublist_querysets.get_volumes_queryset(concept).count()

        context['size'] = concept.issues.aggregate(v=Sum('size'))['v']

        context.update(get_first_page('issues', sublist_querysets.get_issues_queryset(concept)))
        context.update(get_first_page('volumes', sublist_querysets.get_volumes_queryset(concept)))

        context['missing_issues_count'] = concept.missing_issues.filter(skip=False).count()

        if self.request.user.is_authenticated:
            context['watched'] = self.object.watchers.filter(user=self.request.user).exists()

        return context


concept_detail_view = ConceptDetailView.as_view()


class StartWatchView(BaseStartWatchView):
    model = Concept
    MISSING_ISSUES_TASK = 'read_comics.missing_issues.tasks.ConceptMissingIssuesTask'


start_watch_view = StartWatchView.as_view()


class StopWatchView(BaseStopWatchView):
    model = Concept


stop_watch_view = StopWatchView.as_view()


@logging.methods_logged(logger, ['get', ])
class ConceptIssuesListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getIssuesPage",
        'url_template_name': "concepts/badges_urls/issue.html"
    }
    get_queryset_func = staticmethod(sublist_querysets.get_issues_queryset)
    parent_model = Concept


concept_issues_list_view = ConceptIssuesListView.as_view()


@logging.methods_logged(logger, ['get', ])
class ConceptVolumesListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getVolumesPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.get_volumes_queryset)
    parent_model = Concept


concept_volumes_list_view = ConceptVolumesListView.as_view()


@logging.methods_logged(logger, ['get', ])
class ConceptIssueDetailView(IssueDetailView):
    slug_url_kwarg = 'issue_slug'
    slug_field = 'slug'
    active_menu_item = 'concepts'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.concept = None

    def get_queryset(self):
        self.concept = get_object_or_404(Concept, slug=self.kwargs.get('concept_slug'))
        self.base_queryset = self.concept.issues.all()
        return self.base_queryset.select_related('volume', 'volume__publisher')

    def get_ordering(self):
        return 'cover_date'

    def issue_to_url(self, issue):
        return reverse_lazy('concepts:issue_detail', args=(self.concept.slug, issue.slug))

    def get_breadcrumb(self):
        concept = self.concept
        issue = self.object

        return [
            {'url': reverse_lazy("concepts:list"), 'text': 'Concepts'},
            {
                'url': concept.get_absolute_url(),
                'text': concept.name
            },
            {
                'url': reverse_lazy("concepts:issue_detail", args=(concept.slug, issue.slug)),
                'text': f"{issue.volume.name} ({issue.volume.start_year}) #{issue.number}"
            }
        ]


concept_issue_detail_view = ConceptIssueDetailView.as_view()


@logging.methods_logged(logger, ['get', ])
class ConceptDownloadView(BaseZipDownloadView):
    sublist_querysets = sublist_querysets
    base_model = Concept


concept_download_view = ConceptDownloadView.as_view()
