from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from issues.view_mixins import IssuesViewMixin
from issues.views import IssueDetailView
from utils import logging
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
from read_comics.volumes.view_mixins import VolumesViewMixin

from . import sublist_querysets
from .models import Location

logger = logging.getLogger(__name__)


@logging.methods_logged(logger, ["get", ])
class LocationsListView(ElidedPagesPaginatorMixin, ActiveMenuMixin, OnlyWithIssuesMixin, OrderingMixin, BreadcrumbMixin,
                        ListView):
    context_object_name = "locations"
    template_name = "locations/list.html"
    breadcrumb = [{"url": reverse_lazy("locations:list"), "text": "Locations"}]
    paginate_by = 48
    possible_order = ("issue_count", "-issue_count", "volume_count", "-volume_count", "name", "-name")
    default_ordering = "name"
    queryset = Location.objects.was_matched().annotate(
        volume_count=Count("issues__volume", distinct=True)
    ).annotate(
        issue_count=Count("issues", distinct=True)
    )
    active_menu_item = "locations"


locations_list_view = LocationsListView.as_view()


@logging.methods_logged(logger, ["get", ])
class LocationDetailView(IssuesViewMixin, VolumesViewMixin, ActiveMenuMixin, BreadcrumbMixin, DetailView):
    model = Location
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "location"
    template_name = "locations/detail.html"
    active_menu_item = "locations"
    sublist_querysets = sublist_querysets.LocationSublistQueryset()

    def get_breadcrumb(self):
        location = self.object
        return [
            {"url": reverse_lazy("locations:list"), "text": "Locations"},
            {"url": "#",
             "text": location.name}
        ]

    def get_context_data(self, **kwargs):
        context = super(LocationDetailView, self).get_context_data(**kwargs)
        location = self.object
        context["missing_issues_count"] = location.missing_issues.count()

        if self.request.user.is_authenticated:
            context["watched"] = self.object.watchers.filter(user=self.request.user).exists()

        return context


location_detail_view = LocationDetailView.as_view()


class StartWatchView(BaseStartWatchView):
    model = Location
    MISSING_ISSUES_TASK = "read_comics.missing_issues.tasks.LocationMissingIssuesTask"


start_watch_view = StartWatchView.as_view()


class StopWatchView(BaseStopWatchView):
    model = Location


stop_watch_view = StopWatchView.as_view()


@logging.methods_logged(logger, ["get", ])
class LocationIssuesListView(BaseSublistView):
    extra_context = {
        "get_page_function": "getIssuesPage",
        "url_template_name": "concepts/badges_urls/issue.html",
        "break_groups": True
    }
    get_queryset_func = staticmethod(sublist_querysets.LocationSublistQueryset().get_issues_queryset)
    get_queryset_user_param = True
    parent_model = Location


location_issues_list_view = LocationIssuesListView.as_view()


@logging.methods_logged(logger, ["get", ])
class LocationVolumesListView(BaseSublistView):
    extra_context = {
        "get_page_function": "getVolumesPage",
        "break_groups": True
    }
    get_queryset_func = staticmethod(sublist_querysets.LocationSublistQueryset().get_volumes_queryset)
    parent_model = Location
    get_queryset_user_param = True


location_volumes_list_view = LocationVolumesListView.as_view()


@logging.methods_logged(logger, ["get", ])
class LocationIssueDetailView(IssueDetailView):
    slug_url_kwarg = "issue_slug"
    slug_field = "slug"
    active_menu_item = "locations"

    def get_queryset(self):
        self.base_object = get_object_or_404(Location, slug=self.kwargs.get("location_slug"))
        self.base_queryset = self.base_object.issues.all()
        return self.base_queryset.select_related("volume", "volume__publisher")

    def get_ordering(self):
        return "cover_date"

    def issue_to_url(self, issue):
        return reverse_lazy("locations:issue_detail", args=(self.base_object.slug, issue.slug))

    def get_breadcrumb(self):
        location = self.base_object
        issue = self.object

        return [
            {"url": reverse_lazy("locations:list"), "text": "Locations"},
            {
                "url": location.get_absolute_url(),
                "text": location.name
            },
            {
                "url": reverse_lazy("locations:issue_detail", args=(location.slug, issue.slug)),
                "text": f"{issue.volume.name} ({issue.volume.start_year}) #{issue.number}"
            }
        ]


location_issue_detail_view = LocationIssueDetailView.as_view()


@logging.methods_logged(logger, ["get", ])
class LocationDownloadView(BaseZipDownloadView):
    sublist_querysets = sublist_querysets
    base_model = Location


location_download_view = LocationDownloadView.as_view()
