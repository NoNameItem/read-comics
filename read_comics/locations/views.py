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
from .models import Location

logger = logging.getLogger(__name__)


@logging.methods_logged(logger, ['get', ])
class LocationsListView(ElidedPagesPaginatorMixin, ActiveMenuMixin, OnlyWithIssuesMixin, OrderingMixin, BreadcrumbMixin,
                        ListView):
    context_object_name = "locations"
    template_name = "locations/list.html"
    breadcrumb = [{'url': reverse_lazy("locations:list"), 'text': 'Locations'}]
    paginate_by = 48
    possible_order = ('issue_count', '-issue_count', 'volume_count', '-volume_count', 'name', '-name')
    default_ordering = 'name'
    queryset = Location.objects.was_matched().annotate(
        volume_count=Count('issues__volume', distinct=True)
    ).annotate(
        issue_count=Count('issues', distinct=True)
    )
    active_menu_item = 'locations'


locations_list_view = LocationsListView.as_view()


@logging.methods_logged(logger, ['get', ])
class LocationDetailView(ActiveMenuMixin, BreadcrumbMixin, DetailView):
    model = Location
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "location"
    template_name = "locations/detail.html"
    active_menu_item = 'locations'

    def get_breadcrumb(self):
        location = self.object
        return [
            {'url': reverse_lazy("locations:list"), 'text': 'Locations'},
            {'url': '#',
             'text': location.name}
        ]

    def get_context_data(self, **kwargs):
        context = super(LocationDetailView, self).get_context_data(**kwargs)
        location = self.object

        context['issues_count'] = sublist_querysets.get_issues_queryset(location).count()
        context['volumes_count'] = sublist_querysets.get_volumes_queryset(location).count()

        context['size'] = location.issues.aggregate(v=Sum('size'))['v']

        context.update(get_first_page('issues', sublist_querysets.get_issues_queryset(location, self.request.user)))
        context.update(get_first_page('volumes', sublist_querysets.get_volumes_queryset(location)))

        context['missing_issues_count'] = location.missing_issues.count()

        if self.request.user.is_authenticated:
            context['watched'] = self.object.watchers.filter(user=self.request.user).exists()

        return context


location_detail_view = LocationDetailView.as_view()


class StartWatchView(BaseStartWatchView):
    model = Location
    MISSING_ISSUES_TASK = 'read_comics.missing_issues.tasks.LocationMissingIssuesTask'


start_watch_view = StartWatchView.as_view()


class StopWatchView(BaseStopWatchView):
    model = Location


stop_watch_view = StopWatchView.as_view()


@logging.methods_logged(logger, ['get', ])
class LocationIssuesListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getIssuesPage",
        'url_template_name': "concepts/badges_urls/issue.html",
        'break_groups': True
    }
    get_queryset_func = staticmethod(sublist_querysets.get_issues_queryset)
    get_queryset_user_param = True
    parent_model = Location


location_issues_list_view = LocationIssuesListView.as_view()


@logging.methods_logged(logger, ['get', ])
class LocationVolumesListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getVolumesPage",
        'break_groups': True
    }
    get_queryset_func = staticmethod(sublist_querysets.get_volumes_queryset)
    parent_model = Location


location_volumes_list_view = LocationVolumesListView.as_view()


@logging.methods_logged(logger, ['get', ])
class LocationIssueDetailView(IssueDetailView):
    slug_url_kwarg = 'issue_slug'
    slug_field = 'slug'
    active_menu_item = 'locations'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.location = None

    def get_queryset(self):
        self.location = get_object_or_404(Location, slug=self.kwargs.get('location_slug'))
        self.base_queryset = self.location.issues.all()
        return self.base_queryset.select_related('volume', 'volume__publisher')

    def get_ordering(self):
        return 'cover_date'

    def issue_to_url(self, issue):
        return reverse_lazy('locations:issue_detail', args=(self.location.slug, issue.slug))

    def get_breadcrumb(self):
        location = self.location
        issue = self.object

        return [
            {'url': reverse_lazy("locations:list"), 'text': 'Locations'},
            {
                'url': location.get_absolute_url(),
                'text': location.name
            },
            {
                'url': reverse_lazy("locations:issue_detail", args=(location.slug, issue.slug)),
                'text': f"{issue.volume.name} ({issue.volume.start_year}) #{issue.number}"
            }
        ]


location_issue_detail_view = LocationIssueDetailView.as_view()


@logging.methods_logged(logger, ['get', ])
class LocationDownloadView(BaseZipDownloadView):
    sublist_querysets = sublist_querysets
    base_model = Location


location_download_view = LocationDownloadView.as_view()
