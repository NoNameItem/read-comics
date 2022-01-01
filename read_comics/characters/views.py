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
from .models import Character

logger = logging.getLogger(__name__)


@logging.methods_logged(logger, ['get', ])
class CharacterListView(ElidedPagesPaginatorMixin, ActiveMenuMixin, OnlyWithIssuesMixin, OrderingMixin, BreadcrumbMixin,
                        ListView):
    context_object_name = "characters"
    template_name = "characters/list.html"
    breadcrumb = [{'url': reverse_lazy("characters:list"), 'text': 'Characters'}]
    paginate_by = 48
    possible_order = ('issue_count', '-issue_count', 'volume_count', '-volume_count', 'name', '-name')
    default_ordering = 'name'
    queryset = Character.objects.was_matched().annotate(
        volume_count=Count('issues__volume', distinct=True)
    ).annotate(
        issue_count=Count('issues', distinct=True)
    ).select_related('publisher').only(
        'slug',
        'thumb_url',
        'name',
        'publisher__thumb_url',
        'publisher__name',
        'short_description'
    )
    active_menu_item = 'characters'


character_list_view = CharacterListView.as_view()


@logging.methods_logged(logger, ['get', ])
class CharacterDetailView(ActiveMenuMixin, BreadcrumbMixin, DetailView):
    model = Character
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "character"
    template_name = "characters/detail.html"
    active_menu_item = 'characters'

    def get_breadcrumb(self):
        character = self.object
        return [
            {'url': reverse_lazy("characters:list"), 'text': 'Characters'},
            {'url': '#',
             'text': character.name}
        ]

    def get_context_data(self, **kwargs):
        context = super(CharacterDetailView, self).get_context_data(**kwargs)
        character = self.object

        context['issues_count'] = sublist_querysets.get_issues_queryset(character).count()
        context['volumes_count'] = sublist_querysets.get_volumes_queryset(character).count()
        context['died_in_count'] = sublist_querysets.get_died_in_queryset(character).count()
        context['authors_count'] = sublist_querysets.get_authors_queryset(character).count()
        context['enemies_count'] = sublist_querysets.get_character_enemies_queryset(character).count()
        context['friends_count'] = sublist_querysets.get_character_friends_queryset(character).count()
        context['teams_count'] = sublist_querysets.get_teams_queryset(character).count()
        context['team_friends_count'] = sublist_querysets.get_team_friends_queryset(character).count()
        context['team_enemies_count'] = sublist_querysets.get_team_enemies_queryset(character).count()

        context['size'] = character.issues.aggregate(v=Sum('size'))['v']

        context.update(get_first_page('issues', sublist_querysets.get_issues_queryset(character)))
        context.update(get_first_page('volumes', sublist_querysets.get_volumes_queryset(character)))
        context.update(get_first_page('died_in', sublist_querysets.get_died_in_queryset(character)))
        context.update(get_first_page('authors', sublist_querysets.get_authors_queryset(character)))
        context.update(get_first_page('enemies', sublist_querysets.get_character_enemies_queryset(character)))
        context.update(get_first_page('friends', sublist_querysets.get_character_friends_queryset(character)))
        context.update(get_first_page('teams', sublist_querysets.get_teams_queryset(character)))
        context.update(get_first_page('team_friends', sublist_querysets.get_team_friends_queryset(character)))
        context.update(get_first_page('team_enemies', sublist_querysets.get_team_enemies_queryset(character)))

        context['missing_issues_count'] = character.missing_issues.filter(skip=False).count()

        if self.request.user.is_authenticated:
            context['watched'] = self.object.watchers.filter(user=self.request.user).exists()

        return context


character_detail_view = CharacterDetailView.as_view()


class StartWatchView(BaseStartWatchView):
    model = Character
    MISSING_ISSUES_TASK = 'read_comics.missing_issues.tasks.CharacterMissingIssuesTask'


start_watch_view = StartWatchView.as_view()


class StopWatchView(BaseStopWatchView):
    model = Character


stop_watch_view = StopWatchView.as_view()


@logging.methods_logged(logger, ['get', ])
class CharacterIssuesListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getIssuesPage",
        'url_template_name': "characters/badges_urls/issue.html"
    }
    get_queryset_func = staticmethod(sublist_querysets.get_issues_queryset)
    parent_model = Character


character_issues_list_view = CharacterIssuesListView.as_view()


@logging.methods_logged(logger, ['get', ])
class CharacterVolumesListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getVolumesPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.get_volumes_queryset)
    parent_model = Character


character_volumes_list_view = CharacterVolumesListView.as_view()


@logging.methods_logged(logger, ['get', ])
class CharacterDiedInIssuesListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getDiedPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.get_died_in_queryset)
    parent_model = Character


character_died_in_issues_list_view = CharacterDiedInIssuesListView.as_view()


@logging.methods_logged(logger, ['get', ])
class CharacterEnemiesListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getEnemiesPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.get_character_enemies_queryset)
    parent_model = Character


character_enemies_list_view = CharacterEnemiesListView.as_view()


@logging.methods_logged(logger, ['get', ])
class CharacterFriendsListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getFriendsPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.get_character_friends_queryset)
    parent_model = Character


character_friends_list_view = CharacterFriendsListView.as_view()


@logging.methods_logged(logger, ['get', ])
class CharacterTeamsListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getTeamsPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.get_teams_queryset)
    parent_model = Character


character_teams_list_view = CharacterTeamsListView.as_view()


@logging.methods_logged(logger, ['get', ])
class CharacterTeamFriendsListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getTeamFriendsPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.get_team_friends_queryset)
    parent_model = Character


character_team_friends_list_view = CharacterTeamFriendsListView.as_view()


@logging.methods_logged(logger, ['get', ])
class CharacterTeamEnemiesListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getTeamEnemiesPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.get_team_enemies_queryset)
    parent_model = Character


character_team_enemies_list_view = CharacterTeamEnemiesListView.as_view()


@logging.methods_logged(logger, ['get', ])
class CharacterAuthorsListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getAuthorsPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.get_authors_queryset)
    parent_model = Character


character_authors_list_view = CharacterAuthorsListView.as_view()


@logging.methods_logged(logger, ['get', ])
class CharacterIssueDetailView(IssueDetailView):
    slug_url_kwarg = 'issue_slug'
    slug_field = 'slug'
    active_menu_item = 'characters'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.character = None

    def get_queryset(self):
        self.character = get_object_or_404(Character, slug=self.kwargs.get('character_slug'))
        self.base_queryset = self.character.issues.all()
        return self.base_queryset.select_related('volume', 'volume__publisher')

    def get_ordering(self):
        return 'cover_date'

    def issue_to_url(self, issue):
        return reverse_lazy('characters:issue_detail', args=(self.character.slug, issue.slug))

    def get_breadcrumb(self):
        character = self.character
        issue = self.object

        return [
            {'url': reverse_lazy("characters:list"), 'text': 'Characters'},
            {
                'url': self.character.get_absolute_url(),
                'text': character.name
            },
            {
                'url': reverse_lazy("characters:issue_detail", args=(character.slug, issue.slug)),
                'text': f"{issue.volume.name} ({issue.volume.start_year}) #{issue.number}"
            }
        ]


character_issue_detail_view = CharacterIssueDetailView.as_view()


@logging.methods_logged(logger, ['get', ])
class CharacterDownloadView(BaseZipDownloadView):
    sublist_querysets = sublist_querysets
    base_model = Character


character_download_view = CharacterDownloadView.as_view()
