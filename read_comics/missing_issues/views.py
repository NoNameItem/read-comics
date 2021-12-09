from typing import Any

from django import http
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django_magnificent_messages import notifications
from utils import logging
from utils.view_mixins import ActiveMenuMixin, BreadcrumbMixin, IsAdminMixin

from read_comics.characters.models import Character
from read_comics.concepts.models import Concept
from read_comics.locations.models import Location
from read_comics.objects.models import Object
from read_comics.people.models import Person
from read_comics.publishers.models import Publisher
from read_comics.story_arcs.models import StoryArc
from read_comics.teams.models import Team
from read_comics.volumes.models import Volume

from .models import IgnoredIssue, IgnoredPublisher, IgnoredVolume, MissingIssue

logger = logging.getLogger(__name__)


CATEGORY_MODELS = {
    'character': Character,
    'concept': Concept,
    'location': Location,
    'object': Object,
    'person': Person,
    'publisher': Publisher,
    'story_arc': StoryArc,
    'team': Team,
    'volume': Volume
}


@logging.methods_logged(logger, ['setup', 'get', ])
class MissingIssuesListView(IsAdminMixin, BreadcrumbMixin, ActiveMenuMixin, ListView):
    template_name = "missing_issues/missing_issues_list.html"
    active_menu_item = 'missing_issues'
    context_object_name = 'missing_issues'

    breadcrumb = [{'url': reverse_lazy("missing_issues:all"), 'text': 'Missing issues'}]

    def __init__(self, **kwargs: Any):
        super(MissingIssuesListView, self).__init__(**kwargs)
        self.category_key = None
        self.slug = None
        self.obj = None

    def setup(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> None:
        super(MissingIssuesListView, self).setup(request, *args, **kwargs)
        self.category_key = kwargs.get('category', None)
        self.slug = kwargs.get('slug', None)

        if self.category_key:
            try:
                self.obj = CATEGORY_MODELS[self.category_key].objects.get(slug=self.slug)
            except (KeyError, ObjectDoesNotExist):
                raise Http404

    def get_queryset(self) -> QuerySet:
        if self.obj:
            return self.obj.missing_issues.all().order_by(
                'publisher_name',
                'publisher_comicvine_id',
                'volume_name',
                'volume_start_year',
                'volume_comicvine_id',
                'number',
                'comicvine_id'
            )
        else:
            return MissingIssue.objects.all().order_by(
                'publisher_name',
                'publisher_comicvine_id',
                'volume_name',
                'volume_start_year',
                'volume_comicvine_id',
                'number',
                'comicvine_id'
            )

    def get_breadcrumb(self):
        if self.obj:
            return self.breadcrumb + [{'url': '', 'text': str(self.obj)}]
        return self.breadcrumb

    def get_context_data(self, **kwargs):
        context = super(MissingIssuesListView, self).get_context_data(**kwargs)
        context['obj'] = self.obj
        context['category_key'] = self.category_key
        context['missing_issues_count'] = context[self.context_object_name].count()
        context[self.context_object_name] = context[self.context_object_name][:100]
        return context


missing_issues_view = MissingIssuesListView.as_view()


class BaseSkipIgnoreView(IsAdminMixin, View):
    def __init__(self, **kwargs):
        super(BaseSkipIgnoreView, self).__init__(**kwargs)
        self.category_key = None
        self.slug = None
        self.obj = None
        self.object_not_found = False
        self.missing_issue_comicvine_id = None
        self.missing_issue = None
        self.missing_issue_not_found = False

    def setup(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> None:
        super(BaseSkipIgnoreView, self).setup(request, *args, **kwargs)
        self.category_key = kwargs.get('category', None)
        self.slug = kwargs.get('slug', None)
        self.missing_issue_comicvine_id = kwargs.get('comicvine_id')

        if self.category_key:
            try:
                self.obj = CATEGORY_MODELS[self.category_key].objects.get(slug=self.slug)
            except (KeyError, ObjectDoesNotExist):
                self.obj = None
                self.object_not_found = True

        try:
            self.missing_issue = MissingIssue.objects.get(comicvine_id=self.missing_issue_comicvine_id)
        except MissingIssue.DoesNotExist:
            self.missing_issue = None
            self.missing_issue_not_found = True

    def get(self, request, **kwargs):
        if self.object_not_found:
            notifications.error(self.request, "Object not found", "Error")
            return HttpResponseRedirect(reverse_lazy('pages:home'))
        elif self.missing_issue_not_found:
            notifications.error(self.request, f"Missing issue with comicvine_id = {self.missing_issue_comicvine_id} "
                                              f"not found, may be it's already processed", "Error")
        else:
            try:
                self.process()
            except Exception as err:
                logger.error(err)
                notifications.error(self.request, "Please check logs", "Error occurred")

        if self.obj:
            return HttpResponseRedirect(
                reverse_lazy(
                    'missing_issues:category',
                    kwargs={
                        'category': self.category_key,
                        'slug': self.obj.slug
                    }
                )
            )
        else:
            return HttpResponseRedirect(reverse_lazy('missing_issues:all'))

    def process(self):
        raise NotImplementedError


@logging.methods_logged(logger, ['setup', 'get', ])
class SkipIssueView(BaseSkipIgnoreView):
    def process(self):
        self.missing_issue.delete()
        notifications.success(self.request, "Issue skipped")


skip_issue_view = SkipIssueView.as_view()


@logging.methods_logged(logger, ['setup', 'get', ])
class SkipVolumeView(BaseSkipIgnoreView):
    def process(self):
        MissingIssue.objects.filter(volume_comicvine_id=self.missing_issue.volume_comicvine_id).delete()
        notifications.success(self.request, "Volume skipped")


skip_volume_view = SkipVolumeView.as_view()


@logging.methods_logged(logger, ['setup', 'get', ])
class SkipPublisherView(BaseSkipIgnoreView):
    def process(self):
        MissingIssue.objects.filter(publisher_comicvine_id=self.missing_issue.publisher_comicvine_id).delete()
        notifications.success(self.request, "Publisher skipped")


skip_publisher_view = SkipPublisherView.as_view()


@logging.methods_logged(logger, ['setup', 'get', ])
class IgnoreIssueView(BaseSkipIgnoreView):
    def process(self):
        self.missing_issue.ignore()
        notifications.success(self.request, "Issue ignored")


ignore_issue_view = IgnoreIssueView.as_view()


@logging.methods_logged(logger, ['setup', 'get', ])
class IgnoreVolumeView(BaseSkipIgnoreView):
    def process(self):
        self.missing_issue.ignore_volume()
        notifications.success(self.request, "Volume ignored")


ignore_volume_view = IgnoreVolumeView.as_view()


@logging.methods_logged(logger, ['setup', 'get', ])
class IgnorePublisherView(BaseSkipIgnoreView):
    def process(self):
        self.missing_issue.ignore_publisher()
        notifications.success(self.request, "Publisher ignored")


ignore_publisher_view = IgnorePublisherView.as_view()


class IgnoredIssuesListView(IsAdminMixin, BreadcrumbMixin, ActiveMenuMixin, ListView):
    model = IgnoredIssue
    breadcrumb = [{'url': reverse_lazy("missing_issues:ignored_issues"), 'text': 'Ignored issues'}]
    active_menu_item = 'ignored_issues'
    template_name = 'missing_issues/ignored_issues_list.html'
    context_object_name = 'ignored_issues'


ignored_issues_list_view = IgnoredIssuesListView.as_view()


class IgnoredVolumesListView(IsAdminMixin, BreadcrumbMixin, ActiveMenuMixin, ListView):
    model = IgnoredVolume
    breadcrumb = [{'url': reverse_lazy("missing_issues:ignored_volumes"), 'text': 'Ignored volumes'}]
    active_menu_item = 'ignored_volumes'
    template_name = 'missing_issues/ignored_volumes_list.html'
    context_object_name = 'ignored_volumes'


ignored_volumes_list_view = IgnoredVolumesListView.as_view()


class IgnoredPublishersListView(IsAdminMixin, BreadcrumbMixin, ActiveMenuMixin, ListView):
    model = IgnoredPublisher
    breadcrumb = [{'url': reverse_lazy("missing_issues:ignored_publisher"), 'text': 'Ignored publisher'}]
    active_menu_item = 'ignored_publishers'
    template_name = 'missing_issues/ignored_publishers_list.html'
    context_object_name = 'ignored_publishers'


ignored_publishers_list_view = IgnoredPublishersListView.as_view()


class DeleteView(SingleObjectMixin, View):
    redirect_url = None

    def get(self, request, **kwargs):
        obj = self.get_object()
        obj.delete()
        return HttpResponseRedirect(reverse_lazy(self.redirect_url))


class IgnoredIssueDeleteView(DeleteView):
    redirect_url = "missing_issues:ignored_issues"
    model = IgnoredIssue


ignored_issue_delete_view = IgnoredIssueDeleteView.as_view()


class IgnoredVolumeDeleteView(DeleteView):
    redirect_url = "missing_issues:ignored_volumes"
    model = IgnoredVolume


ignored_volume_delete_view = IgnoredVolumeDeleteView.as_view()


class IgnoredPublisherDeleteView(DeleteView):
    redirect_url = "missing_issues:ignored_publisher"
    model = IgnoredPublisher


ignored_publisher_delete_view = IgnoredPublisherDeleteView.as_view()
