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
from .models import Concept

logger = logging.getLogger(__name__)


@logging.methods_logged(logger, ["get", ])
class ConceptsListView(ElidedPagesPaginatorMixin, ActiveMenuMixin, OnlyWithIssuesMixin, OrderingMixin, BreadcrumbMixin,
                       ListView):
    context_object_name = "concepts"
    template_name = "concepts/list.html"
    breadcrumb = [{"url": reverse_lazy("concepts:list"), "text": "Concepts"}]
    paginate_by = 48
    possible_order = ("issue_count", "-issue_count", "volume_count", "-volume_count", "name", "-name")
    default_ordering = "name"
    queryset = Concept.objects.was_matched().annotate(
        volume_count=Count("issues__volume", distinct=True)
    ).annotate(
        issue_count=Count("issues", distinct=True)
    )
    active_menu_item = "concepts"


concepts_list_view = ConceptsListView.as_view()


@logging.methods_logged(logger, ["get", ])
class ConceptDetailView(IssuesViewMixin, VolumesViewMixin, ActiveMenuMixin, BreadcrumbMixin, DetailView):
    model = Concept
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "concept"
    template_name = "concepts/detail.html"
    active_menu_item = "concepts"
    sublist_querysets = sublist_querysets.ConceptSublistQueryset()

    def get_breadcrumb(self):
        concept = self.object
        return [
            {"url": reverse_lazy("concepts:list"), "text": "Concepts"},
            {"url": "#",
             "text": concept.name}
        ]

    def get_context_data(self, **kwargs):
        context = super(ConceptDetailView, self).get_context_data(**kwargs)
        concept = self.object
        context["missing_issues_count"] = concept.missing_issues.filter(skip=False).count()
        if self.request.user.is_authenticated:
            context["watched"] = self.object.watchers.filter(user=self.request.user).exists()

        return context


concept_detail_view = ConceptDetailView.as_view()


class StartWatchView(BaseStartWatchView):
    model = Concept
    MISSING_ISSUES_TASK = "read_comics.missing_issues.tasks.ConceptMissingIssuesTask"


start_watch_view = StartWatchView.as_view()


class StopWatchView(BaseStopWatchView):
    model = Concept


stop_watch_view = StopWatchView.as_view()


@logging.methods_logged(logger, ["get", ])
class ConceptIssuesListView(BaseSublistView):
    extra_context = {
        "get_page_function": "getIssuesPage",
        "url_template_name": "concepts/badges_urls/issue.html",
        "break_groups": True
    }
    get_queryset_func = staticmethod(sublist_querysets.ConceptSublistQueryset().get_issues_queryset)
    get_queryset_user_param = True
    parent_model = Concept


concept_issues_list_view = ConceptIssuesListView.as_view()


@logging.methods_logged(logger, ["get", ])
class ConceptVolumesListView(BaseSublistView):
    extra_context = {
        "get_page_function": "getVolumesPage",
        "break_groups": True
    }
    get_queryset_func = staticmethod(sublist_querysets.ConceptSublistQueryset().get_volumes_queryset)
    parent_model = Concept
    get_queryset_user_param = True


concept_volumes_list_view = ConceptVolumesListView.as_view()


@logging.methods_logged(logger, ["get", ])
class ConceptIssueDetailView(IssueDetailView):
    slug_url_kwarg = "issue_slug"
    slug_field = "slug"
    active_menu_item = "concepts"

    def get_queryset(self):
        self.base_object = get_object_or_404(Concept, slug=self.kwargs.get("concept_slug"))
        self.base_queryset = self.base_object.issues.all()
        return self.base_queryset.select_related("volume", "volume__publisher")

    def get_ordering(self):
        return "cover_date"

    def issue_to_url(self, issue):
        return reverse_lazy("concepts:issue_detail", args=(self.base_object.slug, issue.slug))

    def get_breadcrumb(self):
        concept = self.base_object
        issue = self.object

        return [
            {"url": reverse_lazy("concepts:list"), "text": "Concepts"},
            {
                "url": concept.get_absolute_url(),
                "text": concept.name
            },
            {
                "url": reverse_lazy("concepts:issue_detail", args=(concept.slug, issue.slug)),
                "text": f"{issue.volume.name} ({issue.volume.start_year}) #{issue.number}"
            }
        ]


concept_issue_detail_view = ConceptIssueDetailView.as_view()


@logging.methods_logged(logger, ["get", ])
class ConceptDownloadView(BaseZipDownloadView):
    sublist_querysets = sublist_querysets.ConceptSublistQueryset()
    base_model = Concept


concept_download_view = ConceptDownloadView.as_view()
