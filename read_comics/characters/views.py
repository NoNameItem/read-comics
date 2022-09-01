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
from read_comics.volumes.view_mixins import VolumesViewMixin

from . import sublist_querysets
from .models import Character

logger = logging.getLogger(__name__)


@logging.methods_logged(
    logger,
    [
        "get",
    ],
)
class CharacterListView(
    ElidedPagesPaginatorMixin, ActiveMenuMixin, OnlyWithIssuesMixin, OrderingMixin, BreadcrumbMixin, ListView
):
    context_object_name = "characters"
    template_name = "characters/list.html"
    breadcrumb = [{"url": reverse_lazy("characters:list"), "text": "Characters"}]
    paginate_by = 48
    possible_order = ("issue_count", "-issue_count", "volume_count", "-volume_count", "name", "-name")
    default_ordering = "name"
    queryset = (
        Character.objects.was_matched()
        .annotate(volume_count=Count("issues__volume", distinct=True))
        .annotate(issue_count=Count("issues", distinct=True))
        .select_related("publisher")
        .only("slug", "thumb_url", "name", "publisher__thumb_url", "publisher__name", "short_description")
    )
    active_menu_item = "characters"


character_list_view = CharacterListView.as_view()


@logging.methods_logged(
    logger,
    [
        "get",
    ],
)
class CharacterDetailView(IssuesViewMixin, VolumesViewMixin, ActiveMenuMixin, BreadcrumbMixin, DetailView):
    model = Character
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "character"
    template_name = "characters/detail.html"
    active_menu_item = "characters"
    sublist_querysets = sublist_querysets.CharacterSublistQuerysets()

    def get_breadcrumb(self):
        character = self.object
        return [{"url": reverse_lazy("characters:list"), "text": "Characters"}, {"url": "#", "text": character.name}]

    def get_context_data(self, **kwargs):
        context = super(CharacterDetailView, self).get_context_data(**kwargs)
        character = self.object

        # context["volumes_count"] = self.sublist_querysets.get_volumes_queryset(character).count()
        context["died_in_count"] = self.sublist_querysets.get_died_in_queryset(character).count()
        context["authors_count"] = self.sublist_querysets.get_authors_queryset(character).count()
        context["enemies_count"] = self.sublist_querysets.get_character_enemies_queryset(character).count()
        context["friends_count"] = self.sublist_querysets.get_character_friends_queryset(character).count()
        context["teams_count"] = self.sublist_querysets.get_teams_queryset(character).count()
        context["team_friends_count"] = self.sublist_querysets.get_team_friends_queryset(character).count()
        context["team_enemies_count"] = self.sublist_querysets.get_team_enemies_queryset(character).count()

        # context.update(get_first_page_old("volumes", self.sublist_querysets.get_volumes_queryset(character)))
        context.update(
            get_first_page_old("died_in", self.sublist_querysets.get_died_in_queryset(character, self.request.user))
        )
        context.update(get_first_page_old("authors", self.sublist_querysets.get_authors_queryset(character)))
        context.update(get_first_page_old("enemies", self.sublist_querysets.get_character_enemies_queryset(character)))
        context.update(get_first_page_old("friends", self.sublist_querysets.get_character_friends_queryset(character)))
        context.update(get_first_page_old("teams", self.sublist_querysets.get_teams_queryset(character)))
        context.update(get_first_page_old("team_friends", self.sublist_querysets.get_team_friends_queryset(character)))
        context.update(get_first_page_old("team_enemies", self.sublist_querysets.get_team_enemies_queryset(character)))

        context["missing_issues_count"] = character.missing_issues.filter(skip=False).count()

        if self.request.user.is_authenticated:
            context["watched"] = self.object.watchers.filter(user=self.request.user).exists()

        return context


character_detail_view = CharacterDetailView.as_view()


class StartWatchView(BaseStartWatchView):
    model = Character
    MISSING_ISSUES_TASK = "read_comics.missing_issues.tasks.CharacterMissingIssuesTask"


start_watch_view = StartWatchView.as_view()


class StopWatchView(BaseStopWatchView):
    model = Character


stop_watch_view = StopWatchView.as_view()


@logging.methods_logged(
    logger,
    [
        "get",
    ],
)
class CharacterIssuesListView(BaseSublistView):
    extra_context = {
        "get_page_function": "getIssuesPage",
        "url_template_name": "characters/badges_urls/issue.html",
        "break_groups": True,
    }
    get_queryset_func = staticmethod(sublist_querysets.CharacterSublistQuerysets().get_issues_queryset)
    get_queryset_user_param = True
    parent_model = Character


character_issues_list_view = CharacterIssuesListView.as_view()


@logging.methods_logged(
    logger,
    [
        "get",
    ],
)
class CharacterVolumesListView(BaseSublistView):
    extra_context = {"get_page_function": "getVolumesPage", "break_groups": True}
    get_queryset_func = staticmethod(sublist_querysets.CharacterSublistQuerysets().get_volumes_queryset)
    get_queryset_user_param = True
    parent_model = Character


character_volumes_list_view = CharacterVolumesListView.as_view()


@logging.methods_logged(
    logger,
    [
        "get",
    ],
)
class CharacterDiedInIssuesListView(BaseSublistView):
    extra_context = {
        "get_page_function": "getDiedPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.CharacterSublistQuerysets().get_died_in_queryset)
    parent_model = Character
    get_queryset_user_param = True


character_died_in_issues_list_view = CharacterDiedInIssuesListView.as_view()


@logging.methods_logged(
    logger,
    [
        "get",
    ],
)
class CharacterEnemiesListView(BaseSublistView):
    extra_context = {
        "get_page_function": "getEnemiesPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.CharacterSublistQuerysets().get_character_enemies_queryset)
    parent_model = Character


character_enemies_list_view = CharacterEnemiesListView.as_view()


@logging.methods_logged(
    logger,
    [
        "get",
    ],
)
class CharacterFriendsListView(BaseSublistView):
    extra_context = {
        "get_page_function": "getFriendsPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.CharacterSublistQuerysets().get_character_friends_queryset)
    parent_model = Character


character_friends_list_view = CharacterFriendsListView.as_view()


@logging.methods_logged(
    logger,
    [
        "get",
    ],
)
class CharacterTeamsListView(BaseSublistView):
    extra_context = {
        "get_page_function": "getTeamsPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.CharacterSublistQuerysets().get_teams_queryset)
    parent_model = Character


character_teams_list_view = CharacterTeamsListView.as_view()


@logging.methods_logged(
    logger,
    [
        "get",
    ],
)
class CharacterTeamFriendsListView(BaseSublistView):
    extra_context = {
        "get_page_function": "getTeamFriendsPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.CharacterSublistQuerysets().get_team_friends_queryset)
    parent_model = Character


character_team_friends_list_view = CharacterTeamFriendsListView.as_view()


@logging.methods_logged(
    logger,
    [
        "get",
    ],
)
class CharacterTeamEnemiesListView(BaseSublistView):
    extra_context = {
        "get_page_function": "getTeamEnemiesPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.CharacterSublistQuerysets().get_team_enemies_queryset)
    parent_model = Character


character_team_enemies_list_view = CharacterTeamEnemiesListView.as_view()


@logging.methods_logged(
    logger,
    [
        "get",
    ],
)
class CharacterAuthorsListView(BaseSublistView):
    extra_context = {
        "get_page_function": "getAuthorsPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.CharacterSublistQuerysets().get_authors_queryset)
    parent_model = Character


character_authors_list_view = CharacterAuthorsListView.as_view()


@logging.methods_logged(
    logger,
    [
        "get",
    ],
)
class CharacterIssueDetailView(IssueDetailView):
    slug_url_kwarg = "issue_slug"
    slug_field = "slug"
    active_menu_item = "characters"

    def get_queryset(self):
        self.base_object = get_object_or_404(Character, slug=self.kwargs.get("character_slug"))
        self.base_queryset = self.base_object.issues.matched()
        return self.base_queryset.select_related("volume", "volume__publisher")

    def get_ordering(self):
        return "cover_date"

    def issue_to_url(self, issue):
        return reverse_lazy("characters:issue_detail", args=(self.base_object.slug, issue.slug))

    def get_breadcrumb(self):
        character = self.base_object
        issue = self.object

        return [
            {"url": reverse_lazy("characters:list"), "text": "Characters"},
            {"url": self.base_object.get_absolute_url(), "text": character.name},
            {
                "url": reverse_lazy("characters:issue_detail", args=(character.slug, issue.slug)),
                "text": f"{issue.volume.name} ({issue.volume.start_year}) #{issue.number}",
            },
        ]


character_issue_detail_view = CharacterIssueDetailView.as_view()


@logging.methods_logged(
    logger,
    [
        "get",
    ],
)
class CharacterDownloadView(BaseZipDownloadView):
    sublist_querysets = sublist_querysets.CharacterSublistQuerysets()
    base_model = Character


character_download_view = CharacterDownloadView.as_view()
