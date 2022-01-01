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
from .models import Team

logger = logging.getLogger(__name__)


@logging.methods_logged(logger, ['get', ])
class TeamsListView(ElidedPagesPaginatorMixin, ActiveMenuMixin, OnlyWithIssuesMixin, OrderingMixin, BreadcrumbMixin,
                    ListView):
    context_object_name = "teams"
    template_name = "teams/list.html"
    breadcrumb = [{'url': reverse_lazy("teams:list"), 'text': 'Teams'}]
    paginate_by = 48
    possible_order = ('issue_count', '-issue_count', 'volume_count', '-volume_count', 'name', '-name')
    default_ordering = 'name'
    queryset = Team.objects.was_matched().annotate(
        volume_count=Count('issues__volume', distinct=True)
    ).annotate(
        issue_count=Count('issues', distinct=True)
    ).select_related('publisher')
    active_menu_item = 'teams'


teams_list_view = TeamsListView.as_view()


@logging.methods_logged(logger, ['get', ])
class TeamDetailView(ActiveMenuMixin, BreadcrumbMixin, DetailView):
    model = Team
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "team"
    template_name = "teams/detail.html"
    active_menu_item = 'teams'

    def get_breadcrumb(self):
        team = self.object
        return [
            {'url': reverse_lazy("teams:list"), 'text': 'Teams'},
            {'url': '#',
             'text': team.name}
        ]

    def get_context_data(self, **kwargs):
        context = super(TeamDetailView, self).get_context_data(**kwargs)
        team = self.object

        context['issues_count'] = sublist_querysets.get_issues_queryset(team).count()
        context['volumes_count'] = sublist_querysets.get_volumes_queryset(team).count()
        context['characters_count'] = sublist_querysets.get_characters_queryset(team).count()
        context['enemies_count'] = sublist_querysets.get_character_enemies_queryset(team).count()
        context['friends_count'] = sublist_querysets.get_character_friends_queryset(team).count()
        context['disbanded_in_count'] = sublist_querysets.get_disbanded_in_queryset(team).count()

        context['size'] = team.issues.aggregate(v=Sum('size'))['v']

        context.update(get_first_page('issues', sublist_querysets.get_issues_queryset(team)))
        context.update(get_first_page('volumes', sublist_querysets.get_volumes_queryset(team)))
        context.update(get_first_page('characters', sublist_querysets.get_characters_queryset(team)))
        context.update(get_first_page('friends', sublist_querysets.get_character_friends_queryset(team)))
        context.update(get_first_page('enemies', sublist_querysets.get_character_enemies_queryset(team)))
        context.update(get_first_page('disbanded_in', sublist_querysets.get_disbanded_in_queryset(team)))

        context['missing_issues_count'] = team.missing_issues.filter(skip=False).count()

        if self.request.user.is_authenticated:
            context['watched'] = self.object.watchers.filter(user=self.request.user).exists()

        return context


team_detail_view = TeamDetailView.as_view()


class StartWatchView(BaseStartWatchView):
    model = Team
    MISSING_ISSUES_TASK = 'read_comics.missing_issues.tasks.TeamMissingIssuesTask'


start_watch_view = StartWatchView.as_view()


class StopWatchView(BaseStopWatchView):
    model = Team


stop_watch_view = StopWatchView.as_view()


@logging.methods_logged(logger, ['get', ])
class TeamIssuesListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getIssuesPage",
        'url_template_name': "teams/badges_urls/issue.html"
    }
    get_queryset_func = staticmethod(sublist_querysets.get_issues_queryset)
    parent_model = Team


team_issues_list_view = TeamIssuesListView.as_view()


@logging.methods_logged(logger, ['get', ])
class TeamVolumesListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getVolumesPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.get_volumes_queryset)
    parent_model = Team


team_volumes_list_view = TeamVolumesListView.as_view()


@logging.methods_logged(logger, ['get', ])
class TeamDisbandedInIssuesListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getDiedPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.get_disbanded_in_queryset)
    parent_model = Team


team_disbanded_in_issues_list_view = TeamDisbandedInIssuesListView.as_view()


@logging.methods_logged(logger, ['get', ])
class TeamEnemiesListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getEnemiesPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.get_character_enemies_queryset)
    parent_model = Team


team_enemies_list_view = TeamEnemiesListView.as_view()


@logging.methods_logged(logger, ['get', ])
class TeamFriendsListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getFriendsPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.get_character_friends_queryset)
    parent_model = Team


team_friends_list_view = TeamFriendsListView.as_view()


@logging.methods_logged(logger, ['get', ])
class TeamCharactersListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getCharactersPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.get_characters_queryset)
    parent_model = Team


team_characters_list_view = TeamCharactersListView.as_view()


@logging.methods_logged(logger, ['get', ])
class TeamIssueDetailView(IssueDetailView):
    slug_url_kwarg = 'issue_slug'
    slug_field = 'slug'
    active_menu_item = 'characters'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.team = None

    def get_queryset(self):
        self.team = get_object_or_404(Team, slug=self.kwargs.get('team_slug'))
        self.base_queryset = self.team.issues.all()
        return self.base_queryset.select_related('volume', 'volume__publisher')

    def get_ordering(self):
        return 'cover_date'

    def issue_to_url(self, issue):
        return reverse_lazy('teams:issue_detail', args=(self.team.slug, issue.slug))

    def get_breadcrumb(self):
        return [
            {'url': reverse_lazy("teams:list"), 'text': 'Teams'},
            {
                'url': self.team.get_absolute_url(),
                'text': self.team.name
            },
            {
                'url': reverse_lazy("teams:issue_detail", args=(self.team.slug, self.object.slug)),
                'text': f"{self.object.volume.name} ({self.object.volume.start_year}) #{self.object.number}"
            }
        ]


# noinspection DuplicatedCode
team_issue_detail_view = TeamIssueDetailView.as_view()


@logging.methods_logged(logger, ['get', ])
class TeamDownloadView(BaseZipDownloadView):
    sublist_querysets = sublist_querysets
    base_model = Team


team_download_view = TeamDownloadView.as_view()
