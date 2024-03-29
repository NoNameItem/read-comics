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
from .models import Object

logger = logging.getLogger(__name__)


@logging.methods_logged(
    logger,
    [
        "get",
    ],
)
class ObjectsListView(
    ElidedPagesPaginatorMixin, ActiveMenuMixin, OnlyWithIssuesMixin, OrderingMixin, BreadcrumbMixin, ListView
):
    context_object_name = "objects"
    template_name = "objects/list.html"
    breadcrumb = [{"url": reverse_lazy("objects:list"), "text": "Objects"}]
    paginate_by = 48
    possible_order = ("issue_count", "-issue_count", "volume_count", "-volume_count", "name", "-name")
    default_ordering = "name"
    queryset = (
        Object.objects.was_matched()
        .annotate(volume_count=Count("issues__volume", distinct=True))
        .annotate(issue_count=Count("issues", distinct=True))
    )
    active_menu_item = "objects"


objects_list_view = ObjectsListView.as_view()


@logging.methods_logged(
    logger,
    [
        "get",
    ],
)
class ObjectDetailView(IssuesViewMixin, VolumesViewMixin, ActiveMenuMixin, BreadcrumbMixin, DetailView):
    model = Object
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "object"
    template_name = "objects/detail.html"
    active_menu_item = "objects"
    sublist_querysets = sublist_querysets.ObjectSublistQueryset()

    def get_breadcrumb(self):
        obj = self.object
        return [{"url": reverse_lazy("objects:list"), "text": "Object"}, {"url": "#", "text": obj.name}]

    def get_context_data(self, **kwargs):
        context = super(ObjectDetailView, self).get_context_data(**kwargs)
        obj = self.object

        context["missing_issues_count"] = obj.missing_issues.filter(skip=False).count()

        if self.request.user.is_authenticated:
            context["watched"] = self.object.watchers.filter(user=self.request.user).exists()

        return context


object_detail_view = ObjectDetailView.as_view()


class StartWatchView(BaseStartWatchView):
    model = Object
    MISSING_ISSUES_TASK = "read_comics.missing_issues.tasks.ObjectMissingIssuesTask"


start_watch_view = StartWatchView.as_view()


class StopWatchView(BaseStopWatchView):
    model = Object


stop_watch_view = StopWatchView.as_view()


@logging.methods_logged(
    logger,
    [
        "get",
    ],
)
class ObjectIssuesListView(BaseSublistView):
    extra_context = {
        "get_page_function": "getIssuesPage",
        "url_template_name": "concepts/badges_urls/issue.html",
        "break_groups": True,
    }
    get_queryset_func = staticmethod(sublist_querysets.ObjectSublistQueryset().get_issues_queryset)
    get_queryset_user_param = True
    parent_model = Object


object_issues_list_view = ObjectIssuesListView.as_view()


@logging.methods_logged(
    logger,
    [
        "get",
    ],
)
class ObjectVolumesListView(BaseSublistView):
    extra_context = {"get_page_function": "getVolumesPage", "break_groups": True}
    get_queryset_func = staticmethod(sublist_querysets.ObjectSublistQueryset().get_volumes_queryset)
    parent_model = Object
    get_queryset_user_param = True


object_volumes_list_view = ObjectVolumesListView.as_view()


@logging.methods_logged(
    logger,
    [
        "get",
    ],
)
class ObjectIssueDetailView(IssueDetailView):
    slug_url_kwarg = "issue_slug"
    slug_field = "slug"
    active_menu_item = "objects"

    def get_queryset(self):
        self.base_object = get_object_or_404(Object, slug=self.kwargs.get("object_slug"))
        self.base_queryset = self.base_object.issues.all()
        return self.base_queryset.select_related("volume", "volume__publisher")

    def get_ordering(self):
        return "cover_date"

    def issue_to_url(self, issue):
        return reverse_lazy("objects:issue_detail", args=(self.base_object.slug, issue.slug))

    def get_breadcrumb(self):
        obj = self.base_object
        issue = self.object

        return [
            {"url": reverse_lazy("objects:list"), "text": "Objects"},
            {"url": obj.get_absolute_url(), "text": obj.name},
            {
                "url": reverse_lazy("objects:issue_detail", args=(obj.slug, issue.slug)),
                "text": f"{issue.volume.name} ({issue.volume.start_year}) #{issue.number}",
            },
        ]


object_issue_detail_view = ObjectIssueDetailView.as_view()


@logging.methods_logged(
    logger,
    [
        "get",
    ],
)
class ObjectDownloadView(BaseZipDownloadView):
    sublist_querysets = sublist_querysets.ObjectSublistQueryset()
    base_model = Object


object_download_view = ObjectDownloadView.as_view()
