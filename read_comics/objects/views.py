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
from .models import Object

logger = logging.getLogger(__name__)


@logging.methods_logged(logger, ['get', ])
class ObjectsListView(ElidedPagesPaginatorMixin, ActiveMenuMixin, OnlyWithIssuesMixin, OrderingMixin, BreadcrumbMixin,
                      ListView):
    context_object_name = "objects"
    template_name = "objects/list.html"
    breadcrumb = [{'url': reverse_lazy("objects:list"), 'text': 'Objects'}]
    paginate_by = 48
    possible_order = ('issue_count', '-issue_count', 'volume_count', '-volume_count', 'name', '-name')
    default_ordering = '-issue_count'
    queryset = Object.objects.was_matched().annotate(
        volume_count=Count('issues__volume', distinct=True)
    ).annotate(
        issue_count=Count('issues', distinct=True)
    )
    active_menu_item = 'objects'


objects_list_view = ObjectsListView.as_view()


@logging.methods_logged(logger, ['get', ])
class ObjectDetailView(ActiveMenuMixin, BreadcrumbMixin, DetailView):
    model = Object
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "object"
    template_name = "objects/detail.html"
    active_menu_item = 'objects'

    def get_breadcrumb(self):
        obj = self.object
        return [
            {'url': reverse_lazy("objects:list"), 'text': 'Object'},
            {'url': '#',
             'text': obj.name}
        ]

    def get_context_data(self, **kwargs):
        context = super(ObjectDetailView, self).get_context_data(**kwargs)
        obj = self.object

        context['issues_count'] = sublist_querysets.get_issues_queryset(obj).count()
        context['volumes_count'] = sublist_querysets.get_volumes_queryset(obj).count()

        context['size'] = obj.issues.aggregate(v=Sum('size'))['v']

        context.update(get_first_page('issues', sublist_querysets.get_issues_queryset(obj)))
        context.update(get_first_page('volumes', sublist_querysets.get_volumes_queryset(obj)))

        return context


object_detail_view = ObjectDetailView.as_view()


@logging.methods_logged(logger, ['get', ])
class ObjectIssuesListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getIssuesPage",
        'url_template_name': "concepts/badges_urls/issue.html"
    }
    get_queryset_func = staticmethod(sublist_querysets.get_issues_queryset)
    parent_model = Object


object_issues_list_view = ObjectIssuesListView.as_view()


@logging.methods_logged(logger, ['get', ])
class ObjectVolumesListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getVolumesPage",
    }
    get_queryset_func = staticmethod(sublist_querysets.get_volumes_queryset)
    parent_model = Object


object_volumes_list_view = ObjectVolumesListView.as_view()


@logging.methods_logged(logger, ['get', ])
class ObjectIssueDetailView(IssueDetailView):
    slug_url_kwarg = 'issue_slug'
    slug_field = 'slug'
    active_menu_item = 'objects'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.obj = None

    def get_queryset(self):
        self.obj = get_object_or_404(Object, slug=self.kwargs.get('object_slug'))
        self.base_queryset = self.obj.issues.all()
        return self.base_queryset.select_related('volume', 'volume__publisher')

    def get_ordering(self):
        return 'cover_date'

    def issue_to_url(self, issue):
        return reverse_lazy('objects:issue_detail', args=(self.obj.slug, issue.slug))

    def get_breadcrumb(self):
        obj = self.obj
        issue = self.object

        return [
            {'url': reverse_lazy("objects:list"), 'text': 'Objects'},
            {
                'url': obj.get_absolute_url(),
                'text': obj.name
            },
            {
                'url': reverse_lazy("objects:issue_detail", args=(obj.slug, issue.slug)),
                'text': f"{issue.volume.name} ({issue.volume.start_year}) #{issue.number}"
            }
        ]


object_issue_detail_view = ObjectIssueDetailView.as_view()


@logging.methods_logged(logger, ['get', ])
class ObjectDownloadView(BaseZipDownloadView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.obj = None

    def get_files(self):
        self.obj = get_object_or_404(Object, slug=self.kwargs.get('slug'))
        q = sublist_querysets.get_issues_queryset(self.obj)
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
        return self.escape_file_name(f"{self.obj.name}")


object_download_view = ObjectDownloadView.as_view()
