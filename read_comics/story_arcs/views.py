import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import formats
from django.views import View
from django.views.generic import DetailView, ListView
from issues.view_mixins import IssuesViewMixin
from issues.views import IssueDetailView
from psycopg2 import IntegrityError
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
from read_comics.volumes.view_mixins import VolumesViewMixin

from . import sublist_querysets
from .models import StoryArc

logger = logging.getLogger(__name__)


@logging.methods_logged(
    logger,
    [
        "get",
    ],
)
class StoryArcsListView(
    ElidedPagesPaginatorMixin, ActiveMenuMixin, OnlyWithIssuesMixin, OrderingMixin, BreadcrumbMixin, ListView
):
    context_object_name = "story_arcs"
    template_name = "story_arcs/list.html"
    breadcrumb = [{"url": reverse_lazy("story_arcs:list"), "text": "Story Arcs"}]
    paginate_by = 48
    possible_order = ("issue_count", "-issue_count", "volume_count", "-volume_count", "name", "-name")
    default_ordering = "name"
    queryset = (
        StoryArc.objects.was_matched()
        .annotate(volume_count=Count("issues__volume", distinct=True))
        .annotate(issue_count=Count("issues", distinct=True))
        .select_related("publisher")
    )
    active_menu_item = "story_arcs"

    def get_queryset(self):
        q = super(StoryArcsListView, self).get_queryset()
        if self.request.user.is_authenticated:
            return q.annotate(finished_count=Count("issues", filter=Q(issues__finished_users=self.request.user)))
        return q


story_arcs_list_view = StoryArcsListView.as_view()


class StoryArcsContinueReadingView(StoryArcsListView):
    template_name = "story_arcs/continue_reading.html"
    breadcrumb = [
        {"url": reverse_lazy("story_arcs:list"), "text": "Story Arcs"},
        {"url": reverse_lazy("story_arcs:continue_reading"), "text": "Continue reading"},
    ]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.request.user.started_and_not_finished_story_arcs
        raise PermissionDenied()

    def get_context_data(self, **kwargs):
        context = super(StoryArcsListView, self).get_context_data(**kwargs)
        context["hide_menu"] = True
        return context


story_arcs_continue_reading_view = StoryArcsContinueReadingView.as_view()


@logging.methods_logged(
    logger,
    [
        "get",
    ],
)
class StoryArcDetailView(IssuesViewMixin, VolumesViewMixin, ActiveMenuMixin, BreadcrumbMixin, DetailView):
    model = StoryArc
    queryset = StoryArc.objects.select_related("publisher")
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "story_arc"
    template_name = "story_arcs/detail.html"
    active_menu_item = "story_arcs"
    sublist_querysets = sublist_querysets.StoryArcSublistQuerysets()

    def get_breadcrumb(self):
        story_arc = self.object

        return [{"url": reverse_lazy("story_arcs:list"), "text": "Story Arcs"}, {"url": "#", "text": story_arc.name}]

    def get_context_data(self, **kwargs):
        context = super(StoryArcDetailView, self).get_context_data(**kwargs)
        story_arc = self.object

        context["first_appearance_count"] = self.sublist_querysets.get_first_appearance_queryset(story_arc).count()
        context["characters_count"] = self.sublist_querysets.get_characters_queryset(story_arc).count()
        context["characters_died_count"] = self.sublist_querysets.get_died_queryset(story_arc).count()
        context["concepts_count"] = self.sublist_querysets.get_concepts_queryset(story_arc).count()
        context["locations_count"] = self.sublist_querysets.get_locations_queryset(story_arc).count()
        context["objects_count"] = self.sublist_querysets.get_objects_queryset(story_arc).count()
        context["authors_count"] = self.sublist_querysets.get_authors_queryset(story_arc).count()
        context["teams_count"] = self.sublist_querysets.get_teams_queryset(story_arc).count()
        context["disbanded_teams_count"] = self.sublist_querysets.get_disbanded_queryset(story_arc).count()

        context.update(get_first_page_old("characters", self.sublist_querysets.get_characters_queryset(story_arc)))
        context.update(get_first_page_old("died", self.sublist_querysets.get_died_queryset(story_arc)))
        context.update(get_first_page_old("concepts", self.sublist_querysets.get_concepts_queryset(story_arc)))
        context.update(get_first_page_old("locations", self.sublist_querysets.get_locations_queryset(story_arc)))
        context.update(get_first_page_old("objects", self.sublist_querysets.get_objects_queryset(story_arc)))
        context.update(get_first_page_old("authors", self.sublist_querysets.get_authors_queryset(story_arc)))
        context.update(get_first_page_old("teams", self.sublist_querysets.get_teams_queryset(story_arc)))
        context.update(get_first_page_old("disbanded", self.sublist_querysets.get_disbanded_queryset(story_arc)))
        context.update(
            get_first_page_old("first_appearances", self.sublist_querysets.get_first_appearance_queryset(story_arc))
        )

        context["missing_issues_count"] = story_arc.missing_issues.filter(skip=False).count()

        if self.request.user.is_authenticated:
            context["watched"] = self.object.watchers.filter(user=self.request.user).exists()

        return context


story_arc_detail_view = StoryArcDetailView.as_view()


class StartWatchView(BaseStartWatchView):
    model = StoryArc
    MISSING_ISSUES_TASK = "read_comics.missing_issues.tasks.StoryArcMissingIssuesTask"


start_watch_view = StartWatchView.as_view()


class StopWatchView(BaseStopWatchView):
    model = StoryArc


stop_watch_view = StopWatchView.as_view()


@logging.methods_logged(
    logger,
    [
        "get",
    ],
)
class StoryArcIssuesListView(BaseSublistView):
    extra_context = {
        "get_page_function": "getIssuesPage",
        "url_template_name": "story_arcs/badges_urls/issue.html",
        "break_groups": True,
    }
    get_queryset_func = staticmethod(sublist_querysets.StoryArcSublistQuerysets().get_issues_queryset)
    get_queryset_user_param = True
    parent_model = StoryArc


story_arc_issues_list_view = StoryArcIssuesListView.as_view()


@logging.methods_logged(
    logger,
    [
        "get",
    ],
)
class StoryArcVolumesListView(BaseSublistView):
    extra_context = {"get_page_function": "getVolumesPage", "break_groups": True}
    get_queryset_func = staticmethod(sublist_querysets.StoryArcSublistQuerysets().get_volumes_queryset)
    parent_model = StoryArc
    get_queryset_user_param = True


story_arc_volumes_list_view = StoryArcVolumesListView.as_view()


@logging.methods_logged(
    logger,
    [
        "get",
    ],
)
class StoryArcCharactersListView(BaseSublistView):
    extra_context = {"get_page_function": "getCharactersPage"}
    get_queryset_func = staticmethod(sublist_querysets.StoryArcSublistQuerysets().get_characters_queryset)
    parent_model = StoryArc


story_arc_characters_list_view = StoryArcCharactersListView.as_view()


# noinspection DuplicatedCode
@logging.methods_logged(
    logger,
    [
        "get",
    ],
)
class StoryArcDiedListView(BaseSublistView):
    extra_context = {
        "get_page_function": "getDiedPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.StoryArcSublistQuerysets().get_died_queryset)
    parent_model = StoryArc


story_arc_died_list_view = StoryArcDiedListView.as_view()


@logging.methods_logged(
    logger,
    [
        "get",
    ],
)
class StoryArcConceptsListView(BaseSublistView):
    extra_context = {
        "get_page_function": "getConceptsPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.StoryArcSublistQuerysets().get_concepts_queryset)
    parent_model = StoryArc


story_arc_concepts_list_view = StoryArcConceptsListView.as_view()


@logging.methods_logged(
    logger,
    [
        "get",
    ],
)
class StoryArcLocationsListView(BaseSublistView):
    extra_context = {
        "get_page_function": "getLocationsPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.StoryArcSublistQuerysets().get_locations_queryset)
    parent_model = StoryArc


story_arc_locations_list_view = StoryArcLocationsListView.as_view()


@logging.methods_logged(
    logger,
    [
        "get",
    ],
)
class StoryArcObjectsListView(BaseSublistView):
    extra_context = {
        "get_page_function": "getObjectsPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.StoryArcSublistQuerysets().get_objects_queryset)
    parent_model = StoryArc


story_arc_objects_list_view = StoryArcObjectsListView.as_view()


@logging.methods_logged(
    logger,
    [
        "get",
    ],
)
class StoryArcAuthorsListView(BaseSublistView):
    extra_context = {
        "get_page_function": "getAuthorsPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.StoryArcSublistQuerysets().get_authors_queryset)
    parent_model = StoryArc


story_arc_authors_list_view = StoryArcAuthorsListView.as_view()


@logging.methods_logged(
    logger,
    [
        "get",
    ],
)
class StoryArcTeamsListView(BaseSublistView):
    extra_context = {
        "get_page_function": "getTeamsPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.StoryArcSublistQuerysets().get_teams_queryset)
    parent_model = StoryArc


story_arc_teams_list_view = StoryArcTeamsListView.as_view()


@logging.methods_logged(
    logger,
    [
        "get",
    ],
)
class StoryArcDisbandedListView(BaseSublistView):
    extra_context = {
        "get_page_function": "getDisbandedPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.StoryArcSublistQuerysets().get_disbanded_queryset)
    parent_model = StoryArc


story_arc_disbanded_list_view = StoryArcDisbandedListView.as_view()


@logging.methods_logged(
    logger,
    [
        "get",
    ],
)
class StoryArcFirstAppearancesListView(BaseSublistView):
    extra_context = {"get_page_function": "getFirstAppearancesPage", "break_groups": True}
    get_queryset_func = staticmethod(sublist_querysets.StoryArcSublistQuerysets().get_first_appearance_queryset)
    parent_model = StoryArc


story_arc_first_appearances_list_view = StoryArcFirstAppearancesListView.as_view()


@logging.methods_logged(
    logger,
    [
        "get",
    ],
)
class StoryArcIssueDetailView(IssueDetailView):
    slug_url_kwarg = "issue_slug"
    slug_field = "slug"
    active_menu_item = "story_arcs"

    def get_queryset(self):
        self.base_object = get_object_or_404(StoryArc, slug=self.kwargs.get("story_arc_slug"))
        self.base_queryset = self.base_object.issues.all()
        return self.base_queryset.select_related("volume", "volume__publisher")

    def get_ordering(self):
        return "cover_date"

    def issue_to_url(self, issue):
        return reverse_lazy("story_arcs:issue_detail", args=(self.base_object.slug, issue.slug))

    def get_breadcrumb(self):
        return [
            {"url": reverse_lazy("story_arcs:list"), "text": "Story Arcs"},
            {"url": self.base_object.get_absolute_url(), "text": self.base_object.name},
            {
                "url": reverse_lazy("story_arcs:issue_detail", args=(self.base_object.slug, self.object.slug)),
                "text": f"{self.object.volume.name} ({self.object.volume.start_year}) #{self.object.number}",
            },
        ]


story_arc_issue_detail_view = StoryArcIssueDetailView.as_view()


class StoryArcDownloadView(BaseZipDownloadView):
    base_model = StoryArc
    sublist_querysets = sublist_querysets.StoryArcSublistQuerysets()


story_arc_download_view = StoryArcDownloadView.as_view()


class StoryArcMarkFinishedView(View, LoginRequiredMixin):
    def post(self, request, slug):
        try:
            story_arc = get_object_or_404(StoryArc, slug=slug)
            user = request.user
            user.finished_issues.add(*story_arc.issues.all())

            if self.request.user.is_authenticated:
                total_count = story_arc.issues.count()
                finished_count = (
                    story_arc.issues.annotate(
                        finished_flg=Count("finished_users", distinct=True, filter=Q(finished_users=self.request.user))
                    )
                    .exclude(finished_flg=0)
                    .count()
                )
                finished_percent = finished_count / total_count * 100
                finished_stats = render_to_string(
                    "issues/blocks/finished_progress.html",
                    {
                        "finished_count": finished_count,
                        "finished_percent": finished_percent,
                        "total_count": total_count,
                    },
                    request=self.request,
                )
            else:
                finished_stats = ""

            return JsonResponse(
                {
                    "status": "success",
                    "story_arc_name": story_arc.name,
                    "date": formats.localize(datetime.date.today(), use_l10n=True),
                    "finished_stats": finished_stats,
                }
            )
        except IntegrityError:
            return JsonResponse({"status": "error", "message": "You already marked this issue as finished"})
        except Exception as err:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Unknown error, please contact administrator. \n" f"Error message:{err.args[0]}",
                }
            )


story_arc_mark_finished_view = StoryArcMarkFinishedView.as_view()
