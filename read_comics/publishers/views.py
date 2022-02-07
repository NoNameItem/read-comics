from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from issues.view_mixins import IssuesViewMixin
from issues.views import IssueDetailView
from utils import logging
from utils.utils import get_first_page_old
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
from .models import Publisher

logger = logging.getLogger(__name__)


@logging.methods_logged(logger, ["get", ])
class PublisherListView(ElidedPagesPaginatorMixin, ActiveMenuMixin, OnlyWithIssuesMixin, OrderingMixin, BreadcrumbMixin,
                        ListView):
    context_object_name = "publishers"
    template_name = "publishers/list.html"
    breadcrumb = [{"url": reverse_lazy("publishers:list"), "text": "Publishers"}]
    paginate_by = 48
    possible_order = ("issue_count", "-issue_count", "volume_count", "-volume_count", "name", "-name")
    default_ordering = "name"
    queryset = Publisher.objects.was_matched().annotate(
        volume_count=Count("volumes", distinct=True)
    ).annotate(
        issue_count=Count("volumes__issues", distinct=True)
    )
    active_menu_item = "publishers"


publisher_list_view = PublisherListView.as_view()


@logging.methods_logged(logger, ["get", ])
class PublisherDetailView(IssuesViewMixin, ActiveMenuMixin, BreadcrumbMixin, DetailView):
    model = Publisher
    queryset = Publisher.objects.all()
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "publisher"
    template_name = "publishers/detail.html"
    active_menu_item = "publishers"
    sublist_querysets = sublist_querysets

    def get_breadcrumb(self):
        publisher = self.object

        return [
            {"url": reverse_lazy("publishers:list"), "text": "Publishers"},
            {
                "url": "#",
                "text": publisher.name
            }
        ]

    def get_context_data(self, **kwargs):
        context = super(PublisherDetailView, self).get_context_data(**kwargs)
        publisher = self.object

        context["volumes_count"] = sublist_querysets.get_volumes_queryset(publisher).count()
        context["characters_count"] = sublist_querysets.get_characters_queryset(publisher).count()
        context["story_arcs_count"] = sublist_querysets.get_story_arcs_queryset(publisher).count()
        context["teams_count"] = sublist_querysets.get_teams_queryset(publisher).count()

        context.update(get_first_page_old("volumes", sublist_querysets.get_volumes_queryset(publisher)))
        context.update(get_first_page_old("characters", sublist_querysets.get_characters_queryset(publisher)))
        context.update(get_first_page_old("story_arcs", sublist_querysets.get_story_arcs_queryset(publisher)))
        context.update(get_first_page_old("teams", sublist_querysets.get_teams_queryset(publisher)))

        context["missing_issues_count"] = publisher.missing_issues.filter(skip=False).count()

        if self.request.user.is_authenticated:
            context["watched"] = self.object.watchers.filter(user=self.request.user).exists()

        return context


publisher_detail_view = PublisherDetailView.as_view()


class StartWatchView(BaseStartWatchView):
    model = Publisher
    MISSING_ISSUES_TASK = "read_comics.missing_issues.tasks.PublisherMissingIssuesTask"


start_watch_view = StartWatchView.as_view()


class StopWatchView(BaseStopWatchView):
    model = Publisher


stop_watch_view = StopWatchView.as_view()


@logging.methods_logged(logger, ["get", ])
class PublisherIssuesListView(BaseSublistView):
    extra_context = {
        "get_page_function": "getIssuesPage",
        "url_template_name": "publishers/badges_urls/issue.html",
        "break_groups": True
    }
    get_queryset_func = staticmethod(sublist_querysets.get_issues_queryset)
    get_queryset_user_param = True
    parent_model = Publisher


publisher_issues_list_view = PublisherIssuesListView.as_view()


@logging.methods_logged(logger, ["get", ])
class PublisherVolumesListView(BaseSublistView):
    extra_context = {
        "get_page_function": "getVolumesPage",
        "break_groups": True
    }
    get_queryset_func = staticmethod(sublist_querysets.get_volumes_queryset)
    parent_model = Publisher


publisher_volumes_list_view = PublisherVolumesListView.as_view()


@logging.methods_logged(logger, ["get", ])
class PublisherCharactersListView(BaseSublistView):
    extra_context = {
        "get_page_function": "getCharactersPage"
    }
    get_queryset_func = staticmethod(sublist_querysets.get_characters_queryset)
    parent_model = Publisher


publisher_characters_list_view = PublisherCharactersListView.as_view()


@logging.methods_logged(logger, ["get", ])
class PublisherStoryArcsListView(BaseSublistView):
    extra_context = {
        "get_page_function": "getStoryArcsPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.get_story_arcs_queryset)
    parent_model = Publisher


publisher_story_arcs_list_view = PublisherStoryArcsListView.as_view()


@logging.methods_logged(logger, ["get", ])
class PublisherTeamsListView(BaseSublistView):
    extra_context = {
        "get_page_function": "getTeamsPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.get_teams_queryset)
    parent_model = Publisher


publisher_teams_list_view = PublisherTeamsListView.as_view()


@logging.methods_logged(logger, ["get", ])
class PublisherIssueDetailView(IssueDetailView):
    slug_url_kwarg = "issue_slug"
    slug_field = "slug"
    active_menu_item = "publishers"

    def get_queryset(self):
        self.base_object = get_object_or_404(Publisher, slug=self.kwargs.get("publisher_slug"))
        self.base_queryset = sublist_querysets.get_issues_queryset(self.base_object)
        return self.base_queryset.select_related("volume", "volume__publisher")

    def get_ordering(self):
        return "cover_date"

    def issue_to_url(self, issue):
        return reverse_lazy("publishers:issue_detail", args=(self.base_object.slug, issue.slug))

    def get_breadcrumb(self):
        issue = self.object

        return [
            {"url": reverse_lazy("publishers:list"), "text": "Publishers"},
            {
                "url": self.base_object.get_absolute_url(),
                "text": self.base_object
            },
            {
                "url": reverse_lazy("publishers:issue_detail", args=(self.base_object, issue.slug)),
                "text": f"{issue.volume.name} ({issue.volume.start_year}) #{issue.number}"
            }
        ]


publisher_issue_detail_view = PublisherIssueDetailView.as_view()


class PublisherDownloadView(BaseZipDownloadView):
    sublist_querysets = sublist_querysets
    base_model = Publisher


publisher_download_view = PublisherDownloadView.as_view()
