import math

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

from . import sublist_querysets
from .models import Publisher

logger = logging.getLogger(__name__)


@logging.methods_logged(logger, ['get', ])
class PublisherListView(ElidedPagesPaginatorMixin, ActiveMenuMixin, OnlyWithIssuesMixin, OrderingMixin, BreadcrumbMixin,
                        ListView):
    context_object_name = "publishers"
    template_name = "publishers/list.html"
    breadcrumb = [{'url': reverse_lazy("publishers:list"), 'text': 'Publishers'}]
    paginate_by = 48
    possible_order = ('issue_count', '-issue_count', 'volume_count', '-volume_count', 'name', '-name')
    default_ordering = 'name'
    queryset = Publisher.objects.was_matched().annotate(
        volume_count=Count('volumes', distinct=True)
    ).annotate(
        issue_count=Count('volumes__issues', distinct=True)
    )
    active_menu_item = 'publishers'


publisher_list_view = PublisherListView.as_view()


@logging.methods_logged(logger, ['get', ])
class PublisherDetailView(ActiveMenuMixin, BreadcrumbMixin, DetailView):
    model = Publisher
    queryset = Publisher.objects.all()
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "publisher"
    template_name = "publishers/detail.html"
    active_menu_item = 'publishers'

    def get_breadcrumb(self):
        publisher = self.object

        return [
            {'url': reverse_lazy("publishers:list"), 'text': 'Publishers'},
            {
                'url': '#',
                'text': publisher.name
            }
        ]

    def get_context_data(self, **kwargs):
        context = super(PublisherDetailView, self).get_context_data(**kwargs)
        publisher = self.object

        context['issues_count'] = sublist_querysets.get_issues_queryset(publisher).count()
        context['volumes_count'] = sublist_querysets.get_volumes_queryset(publisher).count()
        context['characters_count'] = sublist_querysets.get_characters_queryset(publisher).count()
        context['story_arcs_count'] = sublist_querysets.get_story_arcs_queryset(publisher).count()
        context['teams_count'] = sublist_querysets.get_teams_queryset(publisher).count()

        context['size'] = sublist_querysets.get_issues_queryset(publisher).aggregate(v=Sum('size'))['v']

        context.update(get_first_page('issues', sublist_querysets.get_issues_queryset(publisher)))
        context.update(get_first_page('volumes', sublist_querysets.get_volumes_queryset(publisher)))
        context.update(get_first_page('characters', sublist_querysets.get_characters_queryset(publisher)))
        context.update(get_first_page('story_arcs', sublist_querysets.get_story_arcs_queryset(publisher)))
        context.update(get_first_page('teams', sublist_querysets.get_teams_queryset(publisher)))

        context['missing_issues_count'] = publisher.missing_issues.count()

        return context


publisher_detail_view = PublisherDetailView.as_view()


@logging.methods_logged(logger, ['get', ])
class PublisherIssuesListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getIssuesPage",
        'url_template_name': "publishers/badges_urls/issue.html",
        'break_groups': True
    }
    get_queryset_func = staticmethod(sublist_querysets.get_issues_queryset)
    parent_model = Publisher


publisher_issues_list_view = PublisherIssuesListView.as_view()


@logging.methods_logged(logger, ['get', ])
class PublisherVolumesListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getVolumesPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.get_volumes_queryset)
    parent_model = Publisher


publisher_volumes_list_view = PublisherVolumesListView.as_view()


@logging.methods_logged(logger, ['get', ])
class PublisherCharactersListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getCharactersPage"
    }
    get_queryset_func = staticmethod(sublist_querysets.get_characters_queryset)
    parent_model = Publisher


publisher_characters_list_view = PublisherCharactersListView.as_view()


@logging.methods_logged(logger, ['get', ])
class PublisherStoryArcsListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getStoryArcsPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.get_story_arcs_queryset)
    parent_model = Publisher


publisher_story_arcs_list_view = PublisherStoryArcsListView.as_view()


@logging.methods_logged(logger, ['get', ])
class PublisherTeamsListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getTeamsPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.get_teams_queryset)
    parent_model = Publisher


publisher_teams_list_view = PublisherTeamsListView.as_view()


@logging.methods_logged(logger, ['get', ])
class PublisherIssueDetailView(IssueDetailView):
    slug_url_kwarg = 'issue_slug'
    slug_field = 'slug'
    active_menu_item = 'publishers'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.publisher = None

    def get_queryset(self):
        self.publisher = get_object_or_404(Publisher, slug=self.kwargs.get('publisher_slug'))
        self.base_queryset = sublist_querysets.get_issues_queryset(self.publisher)
        return self.base_queryset.select_related('volume', 'volume__publisher')

    def get_ordering(self):
        return 'cover_date'

    def issue_to_url(self, issue):
        return reverse_lazy('publishers:issue_detail', args=(self.publisher.slug, issue.slug))

    def get_breadcrumb(self):
        issue = self.object

        return [
            {'url': reverse_lazy("publishers:list"), 'text': 'Publishers'},
            {
                'url': self.publisher.get_absolute_url(),
                'text': self.publisher
            },
            {
                'url': reverse_lazy("volumes:issue_detail", args=(self.publisher, issue.slug)),
                'text': f"{issue.volume.name} ({issue.volume.start_year}) #{issue.number}"
            }
        ]


publisher_issue_detail_view = PublisherIssueDetailView.as_view()


class PublisherDownloadView(BaseZipDownloadView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.publisher = None

    def get_files(self):
        self.publisher = get_object_or_404(Publisher, slug=self.kwargs.get('slug'))
        q = sublist_querysets.get_issues_queryset(self.publisher)
        issues_count = q.count()

        if issues_count:
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
        else:
            files = []

        return files

    def get_zip_name(self):
        return self.escape_file_name(self.publisher.name)


publisher_download_view = PublisherDownloadView.as_view()
