import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.db.models import Count, F, Q, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import formats
from django.views import View
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
from .models import Volume

logger = logging.getLogger(__name__)


@logging.methods_logged(logger, ['get', ])
class VolumesListView(ElidedPagesPaginatorMixin, ActiveMenuMixin, OnlyWithIssuesMixin, OrderingMixin, BreadcrumbMixin,
                      ListView):
    context_object_name = "volumes"
    template_name = "volumes/list.html"
    breadcrumb = [{'url': reverse_lazy("volumes:list"), 'text': 'Volumes'}]
    paginate_by = 48
    possible_order = {
        'issue_count': 'issue_count',
        '-issue_count': '-issue_count',
        'name': ('name', 'start_year'),
        '-name': ('-name', '-start_year'),
        'start_year': 'start_year',
        '-start_year': '-start_year'
    }
    default_ordering = 'start_year'
    queryset = Volume.objects.was_matched().annotate(
        issue_count=Count('issues', distinct=True)
    ).select_related('publisher')
    active_menu_item = 'volumes'

    def get_context_data(self, **kwargs):
        context = super(VolumesListView, self).get_context_data(**kwargs)
        ordering = self.request.GET.get('ordering', 'start_year')
        if ordering in ('start_year', '-start_year'):
            context['breaking'] = 'start_year'
        context['hide_finished'] = self.request.GET.get('hide_finished', 'yes')
        return context

    def get_queryset(self):
        q = super(VolumesListView, self).get_queryset()
        if self.request.user.is_authenticated:
            q = q.annotate(
                finished_count=Count('issues', filter=Q(issues__finished_users=self.request.user)))
            if self.request.GET.get('hide_finished', 'yes') == 'yes':
                q = q.exclude(finished_count=F('issue_count'))
        return q


volumes_list_view = VolumesListView.as_view()


@logging.methods_logged(logger, ['get', ])
class VolumeDetailView(ActiveMenuMixin, BreadcrumbMixin, DetailView):
    model = Volume
    queryset = Volume.objects.select_related('publisher')
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "volume"
    template_name = "volumes/detail.html"
    active_menu_item = 'volumes'

    def get_breadcrumb(self):
        volume = self.object

        return [
            {'url': reverse_lazy("volumes:list"), 'text': 'Volumes'},
            {'url': '#',
             'text': f"{volume.name} ({volume.start_year})"}
        ]

    def get_context_data(self, **kwargs):
        context = super(VolumeDetailView, self).get_context_data(**kwargs)
        volume = self.object

        context['issue_count'] = volume.issues.count()

        if self.request.user.is_authenticated:
            context['finished_count'] = volume.issues.filter(finished_users=self.request.user).count()
            context['finished'] = (context['issue_count'] == context['finished_count'])

        context['first_appearance_count'] = sublist_querysets.get_first_appearance_queryset(volume).count()
        context['characters_count'] = sublist_querysets.get_characters_queryset(volume).count()
        context['characters_died_count'] = sublist_querysets.get_died_queryset(volume).count()
        context['concepts_count'] = sublist_querysets.get_concepts_queryset(volume).count()
        context['locations_count'] = sublist_querysets.get_locations_queryset(volume).count()
        context['objects_count'] = sublist_querysets.get_objects_queryset(volume).count()
        context['authors_count'] = sublist_querysets.get_authors_queryset(volume).count()
        context['story_arcs_count'] = sublist_querysets.get_story_arcs_queryset(volume).count()
        context['teams_count'] = sublist_querysets.get_teams_queryset(volume).count()
        context['disbanded_teams_count'] = sublist_querysets.get_disbanded_queryset(volume).count()

        context['size'] = volume.issues.aggregate(v=Sum('size'))['v']

        context.update(get_first_page('issues', sublist_querysets.get_issues_queryset(volume)))
        context.update(get_first_page('characters', sublist_querysets.get_characters_queryset(volume)))
        context.update(get_first_page('died', sublist_querysets.get_died_queryset(volume)))
        context.update(get_first_page('concepts', sublist_querysets.get_concepts_queryset(volume)))
        context.update(get_first_page('locations', sublist_querysets.get_locations_queryset(volume)))
        context.update(get_first_page('objects', sublist_querysets.get_objects_queryset(volume)))
        context.update(get_first_page('authors', sublist_querysets.get_authors_queryset(volume)))
        context.update(get_first_page('story_arcs', sublist_querysets.get_story_arcs_queryset(volume)))
        context.update(get_first_page('teams', sublist_querysets.get_teams_queryset(volume)))
        context.update(get_first_page('disbanded', sublist_querysets.get_disbanded_queryset(volume)))
        context.update(get_first_page('first_appearances', sublist_querysets.get_first_appearance_queryset(volume)))

        context['missing_issues_count'] = volume.missing_issues.count()

        return context


volume_detail_view = VolumeDetailView.as_view()


@logging.methods_logged(logger, ['get', ])
class VolumeIssuesListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getIssuesPage",
        'url_template_name': "volumes/badges_urls/issue.html"
    }
    get_queryset_func = staticmethod(sublist_querysets.get_issues_queryset)
    parent_model = Volume


volume_issues_list_view = VolumeIssuesListView.as_view()


@logging.methods_logged(logger, ['get', ])
class VolumeCharactersListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getCharactersPage"
    }
    get_queryset_func = staticmethod(sublist_querysets.get_characters_queryset)
    parent_model = Volume


volume_characters_list_view = VolumeCharactersListView.as_view()


@logging.methods_logged(logger, ['get', ])
class VolumeDiedListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getDiedPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.get_died_queryset)
    parent_model = Volume


volume_died_list_view = VolumeDiedListView.as_view()


@logging.methods_logged(logger, ['get', ])
class VolumeConceptsListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getConceptsPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.get_concepts_queryset)
    parent_model = Volume


volume_concepts_list_view = VolumeConceptsListView.as_view()


@logging.methods_logged(logger, ['get', ])
class VolumeLocationsListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getLocationsPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.get_locations_queryset)
    parent_model = Volume


volume_locations_list_view = VolumeLocationsListView.as_view()


@logging.methods_logged(logger, ['get', ])
class VolumeObjectsListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getObjectsPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.get_objects_queryset)
    parent_model = Volume


volume_objects_list_view = VolumeObjectsListView.as_view()


@logging.methods_logged(logger, ['get', ])
class VolumeAuthorsListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getAuthorsPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.get_authors_queryset)
    parent_model = Volume


volume_authors_list_view = VolumeAuthorsListView.as_view()


@logging.methods_logged(logger, ['get', ])
class VolumeStoryArcsListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getStoryArcsPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.get_story_arcs_queryset)
    parent_model = Volume


volume_story_arcs_list_view = VolumeStoryArcsListView.as_view()


@logging.methods_logged(logger, ['get', ])
class VolumeTeamsListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getTeamsPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.get_teams_queryset)
    parent_model = Volume


volume_teams_list_view = VolumeTeamsListView.as_view()


@logging.methods_logged(logger, ['get', ])
class VolumeDisbandedListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getDisbandedPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.get_disbanded_queryset)
    parent_model = Volume


volume_disbanded_list_view = VolumeDisbandedListView.as_view()


@logging.methods_logged(logger, ['get', ])
class VolumeFirstAppearancesListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getFirstAppearancesPage",
        'break_groups': True
    }
    get_queryset_func = staticmethod(sublist_querysets.get_first_appearance_queryset)
    parent_model = Volume


volume_first_appearances_list_view = VolumeFirstAppearancesListView.as_view()


@logging.methods_logged(logger, ['get', ])
class VolumeIssueDetailView(IssueDetailView):
    slug_url_kwarg = 'issue_slug'
    slug_field = 'slug'
    active_menu_item = 'volumes'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.volume = None

    def get_queryset(self):
        self.volume = get_object_or_404(Volume, slug=self.kwargs.get('volume_slug'))
        self.base_queryset = self.volume.issues.all()
        return self.base_queryset.select_related('volume', 'volume__publisher')

    def get_ordering(self):
        return 'name'

    def issue_to_url(self, issue):
        return reverse_lazy('volumes:issue_detail', args=(self.volume.slug, issue.slug))

    def get_breadcrumb(self):
        volume = self.volume
        issue = self.object

        return [
            {'url': reverse_lazy("volumes:list"), 'text': 'Volumes'},
            {
                'url': self.volume.get_absolute_url(),
                'text': f"{volume.name} ({volume.start_year})"
            },
            {
                'url': reverse_lazy("volumes:issue_detail", args=(volume.slug, issue.slug)),
                'text': f"{volume.name} ({volume.start_year}) #{issue.number}"
            }
        ]


volume_issue_detail_view = VolumeIssueDetailView.as_view()


class VolumeDownloadView(BaseZipDownloadView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.volume = None

    def get_files(self):
        self.volume = get_object_or_404(Volume, slug=self.kwargs.get('slug'))
        q = self.volume.issues.order_by('numerical_number', 'number')
        files = [
            (
                self.escape_file_name(f"{self.volume.name} #{x.number} {x.name}".rstrip(' ') + x.space_key[-4:]),
                x.download_link
            )
            for x in q
        ]

        return files

    def get_zip_name(self):
        return self.escape_file_name(f"{self.volume.name} ({self.volume.start_year})")


volume_download_view = VolumeDownloadView.as_view()


class VolumeMarkFinishedView(View, LoginRequiredMixin):
    def post(self, request, slug):
        try:
            volume = get_object_or_404(Volume, slug=slug)
            user = request.user
            user.finished_issues.add(*volume.issues.all())
            # r = MODELS.ReadIssue(profile=profile, issue=issue)
            # r.save()
            return JsonResponse({'status': "success", 'volume_name': f"{volume.name} ({volume.start_year})",
                                 'date': formats.localize(datetime.date.today(), use_l10n=True)
                                 })
        except IntegrityError:
            return JsonResponse({'status': 'error', 'message': 'You already marked this issue as finished'})
        except Exception as err:
            return JsonResponse({'status': 'error', 'message': 'Unknown error, please contact administrator. \n'
                                                               'Error message: %s' % err.args[0]})


volume_mark_finished_view = VolumeMarkFinishedView.as_view()
