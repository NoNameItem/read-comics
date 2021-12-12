from typing import Any, List

from django import http
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from utils import logging
from utils.view_mixins import (
    ActiveMenuMixin,
    BreadcrumbMixin,
    ElidedPagesPaginatorMixin,
    IsAdminMixin,
)

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
class MissingIssuesListView(IsAdminMixin, ElidedPagesPaginatorMixin, BreadcrumbMixin, ActiveMenuMixin, ListView):
    template_name = "missing_issues/missing_issues_list.html"
    template_name_partial = "missing_issues/issues_table.html"
    active_menu_item = 'missing_issues'
    context_object_name = 'missing_issues'
    paginate_by = 100

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

    def get_template_names(self) -> List[str]:
        response_type = self.request.GET.get('response_type')
        if response_type == 'partial':
            return [self.template_name_partial]
        return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super(MissingIssuesListView, self).get_context_data(**kwargs)
        context['obj'] = self.obj
        context['category_key'] = self.category_key
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
            return JsonResponse(status=404, data={'message': "Object not found"})
        elif self.missing_issue_not_found:
            return JsonResponse(status=404,
                                data={
                                    'message': f"Missing issue with comicvine_id = {self.missing_issue_comicvine_id} "
                                               f"not found, may be it's already processed"
                                })
        else:
            try:
                self.process()

            except Exception as err:
                logger.error(err)
                return JsonResponse(status=500, data={'message': "Error occured. Please check logs"})

        if self.obj:
            url = reverse_lazy(
                'missing_issues:category',
                kwargs={
                    'category': self.category_key,
                    'slug': self.obj.slug
                }
            )
        else:
            url = reverse_lazy('missing_issues:all')

        if request.GET.get('page'):
            return HttpResponseRedirect(url + f"?page={request.GET.get('page')}&response_type=partial", )
        else:
            return HttpResponseRedirect(url + '?response_type=partial')

    def process(self):
        raise NotImplementedError


@logging.methods_logged(logger, ['setup', 'get', ])
class SkipIssueView(BaseSkipIgnoreView):
    def process(self):
        self.missing_issue.delete()


skip_issue_view = SkipIssueView.as_view()


@logging.methods_logged(logger, ['setup', 'get', ])
class SkipVolumeView(BaseSkipIgnoreView):
    def process(self):
        MissingIssue.objects.filter(volume_comicvine_id=self.missing_issue.volume_comicvine_id).delete()


skip_volume_view = SkipVolumeView.as_view()


@logging.methods_logged(logger, ['setup', 'get', ])
class SkipPublisherView(BaseSkipIgnoreView):
    def process(self):
        MissingIssue.objects.filter(publisher_comicvine_id=self.missing_issue.publisher_comicvine_id).delete()


skip_publisher_view = SkipPublisherView.as_view()


@logging.methods_logged(logger, ['setup', 'get', ])
class IgnoreIssueView(BaseSkipIgnoreView):
    def process(self):
        self.missing_issue.ignore()


ignore_issue_view = IgnoreIssueView.as_view()


@logging.methods_logged(logger, ['setup', 'get', ])
class IgnoreVolumeView(BaseSkipIgnoreView):
    def process(self):
        self.missing_issue.ignore_volume()


ignore_volume_view = IgnoreVolumeView.as_view()


@logging.methods_logged(logger, ['setup', 'get', ])
class IgnorePublisherView(BaseSkipIgnoreView):
    def process(self):
        self.missing_issue.ignore_publisher()


ignore_publisher_view = IgnorePublisherView.as_view()


class IgnoredIssuesListView(IsAdminMixin, ElidedPagesPaginatorMixin, BreadcrumbMixin, ActiveMenuMixin, ListView):
    queryset = IgnoredIssue.objects.all().order_by('publisher_name', 'volume_name', 'volume_start_year', 'number',
                                                   'cover_date', 'comicvine_id')
    breadcrumb = [{'url': reverse_lazy("missing_issues:ignored_issues"), 'text': 'Ignored issues'}]
    active_menu_item = 'ignored_issues'
    template_name = 'missing_issues/ignored_issues_list.html'
    context_object_name = 'ignored_issues'
    paginate_by = 100


ignored_issues_list_view = IgnoredIssuesListView.as_view()


class IgnoredVolumesListView(IsAdminMixin, ElidedPagesPaginatorMixin, BreadcrumbMixin, ActiveMenuMixin, ListView):
    queryset = IgnoredVolume.objects.all().order_by('publisher_name', 'name', 'start_year', 'comicvine_id')
    breadcrumb = [{'url': reverse_lazy("missing_issues:ignored_volumes"), 'text': 'Ignored volumes'}]
    active_menu_item = 'ignored_volumes'
    template_name = 'missing_issues/ignored_volumes_list.html'
    context_object_name = 'ignored_volumes'
    paginate_by = 100


ignored_volumes_list_view = IgnoredVolumesListView.as_view()


class IgnoredPublishersListView(IsAdminMixin, ElidedPagesPaginatorMixin, BreadcrumbMixin, ActiveMenuMixin, ListView):
    queryset = IgnoredPublisher.objects.all().order_by('name')
    breadcrumb = [{'url': reverse_lazy("missing_issues:ignored_publisher"), 'text': 'Ignored publisher'}]
    active_menu_item = 'ignored_publishers'
    template_name = 'missing_issues/ignored_publishers_list.html'
    context_object_name = 'ignored_publishers'
    paginate_by = 100


ignored_publishers_list_view = IgnoredPublishersListView.as_view()


class DeleteView(SingleObjectMixin, View):
    redirect_url = None

    def get(self, request, **kwargs):
        obj = self.get_object()
        obj.delete()
        if request.GET.get('page'):
            return HttpResponseRedirect(reverse_lazy(self.redirect_url) + f"?page={request.GET.get('page')}")
        else:
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
