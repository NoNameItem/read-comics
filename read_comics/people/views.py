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
from .models import Person

logger = logging.getLogger(__name__)


@logging.methods_logged(logger, ['get', ])
class PeopleListView(ElidedPagesPaginatorMixin, ActiveMenuMixin, OnlyWithIssuesMixin, OrderingMixin, BreadcrumbMixin,
                     ListView):
    context_object_name = "people"
    template_name = "people/list.html"
    breadcrumb = [{'url': reverse_lazy("people:list"), 'text': 'People'}]
    paginate_by = 48
    possible_order = ('issue_count', '-issue_count', 'volume_count', '-volume_count', 'name', '-name')
    default_ordering = 'name'
    queryset = Person.objects.was_matched().annotate(
        volume_count=Count('issues__volume', distinct=True)
    ).annotate(
        issue_count=Count('issues', distinct=True)
    )
    active_menu_item = 'people'


people_list_view = PeopleListView.as_view()


@logging.methods_logged(logger, ['get', ])
class PersonDetailView(ActiveMenuMixin, BreadcrumbMixin, DetailView):
    model = Person
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "person"
    template_name = "people/detail.html"
    active_menu_item = 'people'

    def get_breadcrumb(self):
        obj = self.object
        return [
            {'url': reverse_lazy("people:list"), 'text': 'People'},
            {'url': '#',
             'text': obj.name}
        ]

    def get_context_data(self, **kwargs):
        context = super(PersonDetailView, self).get_context_data(**kwargs)
        obj = self.object

        context['issues_count'] = sublist_querysets.get_issues_queryset(obj).count()
        context['volumes_count'] = sublist_querysets.get_volumes_queryset(obj).count()
        context['characters_count'] = obj.created_characters.count()

        context['size'] = obj.issues.aggregate(v=Sum('size'))['v']

        context.update(get_first_page('issues', sublist_querysets.get_issues_queryset(obj, self.request.user)))
        context.update(get_first_page('volumes', sublist_querysets.get_volumes_queryset(obj)))
        context.update(get_first_page('created_characters', obj.created_characters.all()))

        context['missing_issues_count'] = obj.missing_issues.filter(skip=False).count()

        if self.request.user.is_authenticated:
            context['watched'] = self.object.watchers.filter(user=self.request.user).exists()

        return context


person_detail_view = PersonDetailView.as_view()


class StartWatchView(BaseStartWatchView):
    model = Person
    MISSING_ISSUES_TASK = 'read_comics.missing_issues.tasks.PersonMissingIssuesTask'


start_watch_view = StartWatchView.as_view()


class StopWatchView(BaseStopWatchView):
    model = Person


stop_watch_view = StopWatchView.as_view()


@logging.methods_logged(logger, ['get', ])
class PersonIssuesListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getIssuesPage",
        'url_template_name': "people/badges_urls/issue.html",
        'break_groups': True
    }
    get_queryset_func = staticmethod(sublist_querysets.get_issues_queryset)
    get_queryset_user_param = True
    parent_model = Person


person_issues_list_view = PersonIssuesListView.as_view()


@logging.methods_logged(logger, ['get', ])
class PersonVolumesListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getVolumesPage",
        'break_groups': True
    }
    get_queryset_func = staticmethod(sublist_querysets.get_volumes_queryset)
    parent_model = Person


person_volumes_list_view = PersonVolumesListView.as_view()


@logging.methods_logged(logger, ['get', ])
class PersonCharactersListView(BaseSublistView):
    extra_context = {
        'get_page_function': "getCharactersPage"
    }
    get_queryset_func = staticmethod(sublist_querysets.get_characters_queryset)
    parent_model = Person


person_characters_list_view = PersonCharactersListView.as_view()


@logging.methods_logged(logger, ['get', ])
class PersonIssueDetailView(IssueDetailView):
    slug_url_kwarg = 'issue_slug'
    slug_field = 'slug'
    active_menu_item = 'people'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.person = None

    def get_queryset(self):
        self.person = get_object_or_404(Person, slug=self.kwargs.get('person_slug'))
        self.base_queryset = self.person.issues.all()
        return self.base_queryset.select_related('volume', 'volume__publisher')

    def get_ordering(self):
        return 'cover_date'

    def issue_to_url(self, issue):
        return reverse_lazy('people:issue_detail', args=(self.person.slug, issue.slug))

    def get_breadcrumb(self):
        person = self.person
        issue = self.object

        return [
            {'url': reverse_lazy("people:list"), 'text': 'People'},
            {
                'url': person.get_absolute_url(),
                'text': person.name
            },
            {
                'url': reverse_lazy("people:issue_detail", args=(person.slug, issue.slug)),
                'text': f"{issue.volume.name} ({issue.volume.start_year}) #{issue.number}"
            }
        ]


person_issue_detail_view = PersonIssueDetailView.as_view()


@logging.methods_logged(logger, ['get', ])
class PersonDownloadView(BaseZipDownloadView):
    sublist_querysets = sublist_querysets
    base_model = Person


person_download_view = PersonDownloadView.as_view()
