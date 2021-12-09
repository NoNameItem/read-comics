import datetime
import math

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import formats
from django.views import View
from django.views.generic import DetailView, ListView
from issues.views import IssueDetailView
from psycopg2 import IntegrityError
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
from .models import StoryArc

logger = logging.getLogger(__name__)


@logging.methods_logged(logger, ['get', ])
class StoryArcsListView(ElidedPagesPaginatorMixin, ActiveMenuMixin, OnlyWithIssuesMixin, OrderingMixin, BreadcrumbMixin,
                        ListView):
    context_object_name = "story_arcs"
    template_name = "story_arcs/list.html"
    breadcrumb = [{'url': reverse_lazy("story_arcs:list"), 'text': 'Story Arcs'}]
    paginate_by = 48
    possible_order = ('issue_count', '-issue_count', 'volume_count', '-volume_count', 'name', '-name')
    default_ordering = 'name'
    queryset = StoryArc.objects.was_matched().annotate(
        volume_count=Count('issues__volume', distinct=True)
    ).annotate(
        issue_count=Count('issues', distinct=True)
    ).select_related('publisher')
    active_menu_item = 'story_arcs'

    def get_queryset(self):
        q = super(StoryArcsListView, self).get_queryset()
        if self.request.user.is_authenticated:
            q = q.annotate(
                finished_count=Count('issues', filter=Q(issues__finished_users=self.request.user)))
        return q


story_arcs_list_view = StoryArcsListView.as_view()


@logging.methods_logged(logger, ['get', ])
class StoryArcDetailView(ActiveMenuMixin, BreadcrumbMixin, DetailView):
    model = StoryArc
    queryset = StoryArc.objects.select_related('publisher')
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "story_arc"
    template_name = "story_arcs/detail.html"
    active_menu_item = 'story_arcs'

    def get_breadcrumb(self):
        story_arc = self.object

        return [
            {'url': reverse_lazy("story_arcs:list"), 'text': 'Story Arcs'},
            {'url': '#',
             'text': story_arc.name}
        ]

    def get_context_data(self, **kwargs):
        context = super(StoryArcDetailView, self).get_context_data(**kwargs)
        story_arc = self.object

        context['issue_count'] = story_arc.issues.count()

        if self.request.user.is_authenticated:
            context['finished_count'] = story_arc.issues.filter(finished_users=self.request.user).count()
            context['finished'] = (context['issue_count'] == context['finished_count'])

        context['volumes_count'] = sublist_querysets.get_volumes_queryset(story_arc).count()
        context['first_appearance_count'] = sublist_querysets.get_first_appearance_queryset(story_arc).count()
        context['characters_count'] = sublist_querysets.get_characters_queryset(story_arc).count()
        context['characters_died_count'] = sublist_querysets.get_died_queryset(story_arc).count()
        context['concepts_count'] = sublist_querysets.get_concepts_queryset(story_arc).count()
        context['locations_count'] = sublist_querysets.get_locations_queryset(story_arc).count()
        context['objects_count'] = sublist_querysets.get_objects_queryset(story_arc).count()
        context['authors_count'] = sublist_querysets.get_authors_queryset(story_arc).count()
        context['teams_count'] = sublist_querysets.get_teams_queryset(story_arc).count()
        context['disbanded_teams_count'] = sublist_querysets.get_disbanded_queryset(story_arc).count()

        context['size'] = story_arc.issues.aggregate(v=Sum('size'))['v']

        context.update(get_first_page('issues', sublist_querysets.get_issues_queryset(story_arc)))
        context.update(get_first_page('volumes', sublist_querysets.get_volumes_queryset(story_arc)))
        context.update(get_first_page('characters', sublist_querysets.get_characters_queryset(story_arc)))
        context.update(get_first_page('died', sublist_querysets.get_died_queryset(story_arc)))
        context.update(get_first_page('concepts', sublist_querysets.get_concepts_queryset(story_arc)))
        context.update(get_first_page('locations', sublist_querysets.get_locations_queryset(story_arc)))
        context.update(get_first_page('objects', sublist_querysets.get_objects_queryset(story_arc)))
        context.update(get_first_page('authors', sublist_querysets.get_authors_queryset(story_arc)))
        context.update(get_first_page('teams', sublist_querysets.get_teams_queryset(story_arc)))
        context.update(get_first_page('disbanded', sublist_querysets.get_disbanded_queryset(story_arc)))
        context.update(get_first_page('first_appearances', sublist_querysets.get_first_appearance_queryset(story_arc)))

        context['missing_issues_count'] = story_arc.missing_issues.count()

        return context


story_arc_detail_view = StoryArcDetailView.as_view()


@logging.methods_logged(logger, ['get', ])
class StoryArcIssuesListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getIssuesPage",
        'url_template_name': "story_arcs/badges_urls/issue.html"
    }
    get_queryset_func = staticmethod(sublist_querysets.get_issues_queryset)
    parent_model = StoryArc


story_arc_issues_list_view = StoryArcIssuesListView.as_view()


@logging.methods_logged(logger, ['get', ])
class StoryArcVolumesListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getVolumesPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.get_volumes_queryset)
    parent_model = StoryArc


story_arc_volumes_list_view = StoryArcVolumesListView.as_view()


@logging.methods_logged(logger, ['get', ])
class StoryArcCharactersListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getCharactersPage"
    }
    get_queryset_func = staticmethod(sublist_querysets.get_characters_queryset)
    parent_model = StoryArc


story_arc_characters_list_view = StoryArcCharactersListView.as_view()


# noinspection DuplicatedCode
@logging.methods_logged(logger, ['get', ])
class StoryArcDiedListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getDiedPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.get_died_queryset)
    parent_model = StoryArc


story_arc_died_list_view = StoryArcDiedListView.as_view()


@logging.methods_logged(logger, ['get', ])
class StoryArcConceptsListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getConceptsPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.get_concepts_queryset)
    parent_model = StoryArc


story_arc_concepts_list_view = StoryArcConceptsListView.as_view()


@logging.methods_logged(logger, ['get', ])
class StoryArcLocationsListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getLocationsPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.get_locations_queryset)
    parent_model = StoryArc


story_arc_locations_list_view = StoryArcLocationsListView.as_view()


@logging.methods_logged(logger, ['get', ])
class StoryArcObjectsListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getObjectsPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.get_objects_queryset)
    parent_model = StoryArc


story_arc_objects_list_view = StoryArcObjectsListView.as_view()


@logging.methods_logged(logger, ['get', ])
class StoryArcAuthorsListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getAuthorsPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.get_authors_queryset)
    parent_model = StoryArc


story_arc_authors_list_view = StoryArcAuthorsListView.as_view()


@logging.methods_logged(logger, ['get', ])
class StoryArcTeamsListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getTeamsPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.get_teams_queryset)
    parent_model = StoryArc


story_arc_teams_list_view = StoryArcTeamsListView.as_view()


@logging.methods_logged(logger, ['get', ])
class StoryArcDisbandedListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getDisbandedPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.get_disbanded_queryset)
    parent_model = StoryArc


story_arc_disbanded_list_view = StoryArcDisbandedListView.as_view()


@logging.methods_logged(logger, ['get', ])
class StoryArcFirstAppearancesListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getFirstAppearancesPage",
        'break_groups': True
    }
    get_queryset_func = staticmethod(sublist_querysets.get_first_appearance_queryset)
    parent_model = StoryArc


story_arc_first_appearances_list_view = StoryArcFirstAppearancesListView.as_view()


@logging.methods_logged(logger, ['get', ])
class StoryArcIssueDetailView(IssueDetailView):
    slug_url_kwarg = 'issue_slug'
    slug_field = 'slug'
    active_menu_item = 'story_arcs'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.story_arc = None

    def get_queryset(self):
        self.story_arc = get_object_or_404(StoryArc, slug=self.kwargs.get('story_arc_slug'))
        self.base_queryset = self.story_arc.issues.all()
        return self.base_queryset.select_related('volume', 'volume__publisher')

    def get_ordering(self):
        return 'cover_date'

    def issue_to_url(self, issue):
        return reverse_lazy('story_arcs:issue_detail', args=(self.story_arc.slug, issue.slug))

    def get_breadcrumb(self):
        return [
            {'url': reverse_lazy("story_arcs:list"), 'text': 'Story Arcs'},
            {
                'url': self.story_arc.get_absolute_url(),
                'text': self.story_arc.name
            },
            {
                'url': reverse_lazy("story_arcs:issue_detail", args=(self.story_arc.slug, self.object.slug)),
                'text': f"{self.object.volume.name} ({self.object.volume.start_year}) #{self.object.number}"
            }
        ]


story_arc_issue_detail_view = StoryArcIssueDetailView.as_view()


class StoryArcDownloadView(BaseZipDownloadView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.story_arc = None

    def get_files(self):
        self.story_arc = get_object_or_404(StoryArc, slug=self.kwargs.get('slug'))
        q = sublist_querysets.get_issues_queryset(self.story_arc)
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
        return self.escape_file_name(self.story_arc.name)


story_arc_download_view = StoryArcDownloadView.as_view()


class StoryArcMarkFinishedView(View, LoginRequiredMixin):
    def post(self, request, slug):
        try:
            story_arc = get_object_or_404(StoryArc, slug=slug)
            user = request.user
            user.finished_issues.add(*story_arc.issues.all())
            # r = MODELS.ReadIssue(profile=profile, issue=issue)
            # r.save()
            return JsonResponse({'status': "success", 'story_arc_name': story_arc.name,
                                 'date': formats.localize(datetime.date.today(), use_l10n=True)
                                 })
        except IntegrityError:
            return JsonResponse({'status': 'error', 'message': 'You already marked this issue as finished'})
        except Exception as err:
            return JsonResponse({'status': 'error', 'message': 'Unknown error, please contact administrator. \n'
                                                               'Error message: %s' % err.args[0]})


story_arc_mark_finished_view = StoryArcMarkFinishedView.as_view()
