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
from .models import Person

logger = logging.getLogger(__name__)


@logging.methods_logged(logger, ["get", ])
class PeopleListView(ElidedPagesPaginatorMixin, ActiveMenuMixin, OnlyWithIssuesMixin, OrderingMixin, BreadcrumbMixin,
                     ListView):
    context_object_name = "people"
    template_name = "people/list.html"
    breadcrumb = [{"url": reverse_lazy("people:list"), "text": "People"}]
    paginate_by = 48
    possible_order = ("issue_count", "-issue_count", "volume_count", "-volume_count", "name", "-name")
    default_ordering = "name"
    queryset = Person.objects.was_matched().annotate(
        volume_count=Count("issues__volume", distinct=True)
    ).annotate(
        issue_count=Count("issues", distinct=True)
    )
    active_menu_item = "people"


people_list_view = PeopleListView.as_view()


@logging.methods_logged(logger, ["get", ])
class PersonDetailView(IssuesViewMixin, VolumesViewMixin, ActiveMenuMixin, BreadcrumbMixin, DetailView):
    model = Person
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "person"
    template_name = "people/detail.html"
    active_menu_item = "people"
    sublist_querysets = sublist_querysets.PersonSublistQuerysets()

    def get_breadcrumb(self):
        obj = self.object
        return [
            {"url": reverse_lazy("people:list"), "text": "People"},
            {"url": "#",
             "text": obj.name}
        ]

    def get_context_data(self, **kwargs):
        context = super(PersonDetailView, self).get_context_data(**kwargs)
        obj = self.object

        context["characters_count"] = obj.created_characters.count()
        context.update(get_first_page_old("created_characters", obj.created_characters.all()))

        context["missing_issues_count"] = obj.missing_issues.filter(skip=False).count()

        if self.request.user.is_authenticated:
            context["watched"] = self.object.watchers.filter(user=self.request.user).exists()

        return context


person_detail_view = PersonDetailView.as_view()


class StartWatchView(BaseStartWatchView):
    model = Person
    MISSING_ISSUES_TASK = "read_comics.missing_issues.tasks.PersonMissingIssuesTask"


start_watch_view = StartWatchView.as_view()


class StopWatchView(BaseStopWatchView):
    model = Person


stop_watch_view = StopWatchView.as_view()


@logging.methods_logged(logger, ["get", ])
class PersonIssuesListView(BaseSublistView):
    extra_context = {
        "get_page_function": "getIssuesPage",
        "url_template_name": "people/badges_urls/issue.html",
        "break_groups": True
    }
    get_queryset_func = staticmethod(sublist_querysets.PersonSublistQuerysets().get_issues_queryset)
    get_queryset_user_param = True
    parent_model = Person


person_issues_list_view = PersonIssuesListView.as_view()


@logging.methods_logged(logger, ["get", ])
class PersonVolumesListView(BaseSublistView):
    extra_context = {
        "get_page_function": "getVolumesPage",
        "break_groups": True
    }
    get_queryset_func = staticmethod(sublist_querysets.PersonSublistQuerysets().get_volumes_queryset)
    parent_model = Person
    get_queryset_user_param = True


person_volumes_list_view = PersonVolumesListView.as_view()


@logging.methods_logged(logger, ["get", ])
class PersonCharactersListView(BaseSublistView):
    extra_context = {
        "get_page_function": "getCharactersPage"
    }
    get_queryset_func = staticmethod(sublist_querysets.PersonSublistQuerysets().get_characters_queryset)
    parent_model = Person


person_characters_list_view = PersonCharactersListView.as_view()


@logging.methods_logged(logger, ["get", ])
class PersonIssueDetailView(IssueDetailView):
    slug_url_kwarg = "issue_slug"
    slug_field = "slug"
    active_menu_item = "people"

    def get_queryset(self):
        self.base_object = get_object_or_404(Person, slug=self.kwargs.get("person_slug"))
        self.base_queryset = self.base_object.issues.all()
        return self.base_queryset.select_related("volume", "volume__publisher")

    def get_ordering(self):
        return "cover_date"

    def issue_to_url(self, issue):
        return reverse_lazy("people:issue_detail", args=(self.base_object.slug, issue.slug))

    def get_breadcrumb(self):
        person = self.base_object
        issue = self.object

        return [
            {"url": reverse_lazy("people:list"), "text": "People"},
            {
                "url": person.get_absolute_url(),
                "text": person.name
            },
            {
                "url": reverse_lazy("people:issue_detail", args=(person.slug, issue.slug)),
                "text": f"{issue.volume.name} ({issue.volume.start_year}) #{issue.number}"
            }
        ]


person_issue_detail_view = PersonIssueDetailView.as_view()


@logging.methods_logged(logger, ["get", ])
class PersonDownloadView(BaseZipDownloadView):
    sublist_querysets = sublist_querysets
    base_model = Person


person_download_view = PersonDownloadView.as_view()
