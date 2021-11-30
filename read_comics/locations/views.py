import math

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
    default_ordering = '-issue_count'
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

        context.update(get_first_page('issues', sublist_querysets.get_issues_queryset(location)))
        context.update(get_first_page('volumes', sublist_querysets.get_volumes_queryset(location)))

        return context


location_detail_view = LocationDetailView.as_view()


@logging.methods_logged(logger, ['get', ])
class LocationIssuesListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getIssuesPage",
        'url_template_name': "concepts/badges_urls/issue.html"
    }
    get_queryset_func = staticmethod(sublist_querysets.get_issues_queryset)
    parent_model = Location


location_issues_list_view = LocationIssuesListView.as_view()


@logging.methods_logged(logger, ['get', ])
class LocationVolumesListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getVolumesPage",
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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.location = None

    def get_files(self):
        self.location = get_object_or_404(Location, slug=self.kwargs.get('slug'))
        q = sublist_querysets.get_issues_queryset(self.location)
        num_length = math.ceil(math.log10(q.count()))

        files = [
            (
                self.escape_file_name(
                    f"{str(num).rjust(num_length, '0')} - {x.volume.name} #{x.number} {x.name}".rstrip(' ')
                    + x.space_key[-4:]
                ),
                x.download_link
            )
            for num, x in enumerate(q, 1)
        ]

        return files

    def get_zip_name(self):
        return self.escape_file_name(f"{self.location.name}")


location_download_view = LocationDownloadView.as_view()
