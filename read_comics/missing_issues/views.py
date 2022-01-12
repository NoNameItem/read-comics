import datetime
from typing import Any, List

from celery import signature
from django import http
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Q, QuerySet
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django_magnificent_messages import notifications
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
from read_comics.publishers.tasks import publishers_space_task
from read_comics.story_arcs.models import StoryArc
from read_comics.teams.models import Team
from read_comics.volumes.models import Volume

from .models import (
    IgnoredIssue,
    IgnoredPublisher,
    IgnoredVolume,
    MissingIssue,
    WatchedItem,
)
from .queries import get_watched_missing_issues_query

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
    category_skip_publisher_url = "missing_issues:category_skip_publisher"
    category_ignore_publisher_url = "missing_issues:category_skip_publisher"
    category_skip_volume_url = "missing_issues:category_skip_volume"
    category_ignore_volume_url = "missing_issues:category_ignore_volume"
    category_skip_issue_url = "missing_issues:category_skip_issue"
    category_ignore_issue_url = "missing_issues:category_ignore_issue"

    skip_publisher_url = "missing_issues:skip_publisher"
    ignore_publisher_url = "missing_issues:ignore_publisher"
    skip_volume_url = "missing_issues:skip_volume"
    ignore_volume_url = "missing_issues:ignore_volume"
    skip_issue_url = "missing_issues:skip_issue"
    ignore_issue_url = "missing_issues:ignore_issue"

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
            q = self.obj.missing_issues.filter(skip=False).order_by(
                'publisher_name',
                'publisher_comicvine_id',
                'volume_name',
                'volume_start_year',
                'volume_comicvine_id',
                'numerical_number',
                'number',
                'comicvine_id'
            )
        else:
            q = MissingIssue.objects.filter(skip=False).order_by(
                'publisher_name',
                'publisher_comicvine_id',
                'volume_name',
                'volume_start_year',
                'volume_comicvine_id',
                'numerical_number',
                'number',
                'comicvine_id'
            )

        search_query = self.request.GET.get("q")

        if search_query:
            q = q.filter(
                Q(publisher_name__icontains=search_query) |
                Q(volume_name__icontains=search_query) |
                Q(name__icontains=search_query)
            )

        return q.order_by(
            'publisher_name',
            'publisher_comicvine_id',
            'volume_name',
            'volume_start_year',
            'volume_comicvine_id',
            'numerical_number',
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
        context['urls'] = {
            'category_skip_publisher': self.category_skip_publisher_url,
            'category_ignore_publisher': self.category_ignore_publisher_url,
            'category_skip_volume': self.category_skip_volume_url,
            'category_ignore_volume': self.category_ignore_volume_url,
            'category_skip_issue': self.category_skip_issue_url,
            'category_ignore_issue': self.category_ignore_issue_url,
            'skip_publisher': self.skip_publisher_url,
            'ignore_publisher': self.ignore_publisher_url,
            'skip_volume': self.skip_volume_url,
            'ignore_volume': self.ignore_volume_url,
            'skip_issue': self.skip_issue_url,
            'ignore_issue': self.ignore_issue_url
        }
        context['q'] = self.request.GET.get("q")
        return context


missing_issues_list_view = MissingIssuesListView.as_view()


@logging.methods_logged(logger, ['setup', 'get', ])
class WatchedMissingIssuesListView(MissingIssuesListView):
    skip_publisher_url = "missing_issues:watched_skip_publisher"
    ignore_publisher_url = "missing_issues:watched_ignore_publisher"
    skip_volume_url = "missing_issues:watched_skip_volume"
    ignore_volume_url = "missing_issues:watched_ignore_volume"
    skip_issue_url = "missing_issues:watched_skip_issue"
    ignore_issue_url = "missing_issues:watched_ignore_issue"

    breadcrumb = [{'url': reverse_lazy("missing_issues:watched"), 'text': 'Watched missing issues'}]

    def get_queryset(self) -> QuerySet:
        search_query = self.request.GET.get("q")

        return get_watched_missing_issues_query(self.request.user, search_query).order_by(
            'publisher_name',
            'publisher_comicvine_id',
            'volume_name',
            'volume_start_year',
            'volume_comicvine_id',
            'numerical_number',
            'number',
            'comicvine_id'
        )


watched_missing_issues_list_view = WatchedMissingIssuesListView.as_view()


class BaseSkipIgnoreView(IsAdminMixin, View):
    category_redirect_url = 'missing_issues:category'
    redirect_url = 'missing_issues:all'

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
                return JsonResponse(status=500, data={'message': "Error occurred. Please check logs"})

        if self.obj:
            url = reverse_lazy(
                self.category_redirect_url,
                kwargs={
                    'category': self.category_key,
                    'slug': self.obj.slug
                }
            )
        else:
            url = reverse_lazy(self.redirect_url)

        if request.GET.get('page'):
            url = url + f"?page={request.GET.get('page')}&response_type=partial"
        else:
            url = url + '?response_type=partial'

        if request.GET.get("q"):
            url += f"&q={request.GET.get('q')}"

        return HttpResponseRedirect(url)

    def process(self):
        raise NotImplementedError


@logging.methods_logged(logger, ['setup', 'get', ])
class SkipIssueView(BaseSkipIgnoreView):
    def process(self):
        self.missing_issue.skip = True
        self.missing_issue.skip_date = datetime.date.today()
        self.missing_issue.save()


skip_issue_view = SkipIssueView.as_view()


@logging.methods_logged(logger, ['setup', 'get', ])
class WatchedSkipIssueView(SkipIssueView):
    redirect_url = 'missing_issues:watched'


watched_skip_issue_view = WatchedSkipIssueView.as_view()


@logging.methods_logged(logger, ['setup', 'get', ])
class SkipVolumeView(BaseSkipIgnoreView):
    def process(self):
        MissingIssue.objects.filter(volume_comicvine_id=self.missing_issue.volume_comicvine_id).update(
            skip=True,
            skip_date=datetime.date.today()
        )


skip_volume_view = SkipVolumeView.as_view()


@logging.methods_logged(logger, ['setup', 'get', ])
class WatchedSkipVolumeView(SkipVolumeView):
    redirect_url = 'missing_issues:watched'


watched_skip_volume_view = WatchedSkipVolumeView.as_view()


@logging.methods_logged(logger, ['setup', 'get', ])
class SkipPublisherView(BaseSkipIgnoreView):
    def process(self):
        MissingIssue.objects.filter(publisher_comicvine_id=self.missing_issue.publisher_comicvine_id).update(
            skip=True,
            skip_date=datetime.date.today()
        )


skip_publisher_view = SkipPublisherView.as_view()


@logging.methods_logged(logger, ['setup', 'get', ])
class WatchedSkipPublisherView(SkipPublisherView):
    redirect_url = 'missing_issues:watched'


watched_skip_publisher_view = WatchedSkipPublisherView.as_view()


@logging.methods_logged(logger, ['setup', 'get', ])
class IgnoreIssueView(BaseSkipIgnoreView):
    def process(self):
        self.missing_issue.ignore()


ignore_issue_view = IgnoreIssueView.as_view()


@logging.methods_logged(logger, ['setup', 'get', ])
class WatchedIgnoreIssueView(IgnoreIssueView):
    redirect_url = 'missing_issues:watched'


watched_ignore_issue_view = WatchedIgnoreIssueView.as_view()


@logging.methods_logged(logger, ['setup', 'get', ])
class IgnoreVolumeView(BaseSkipIgnoreView):
    def process(self):
        self.missing_issue.ignore_volume()


ignore_volume_view = IgnoreVolumeView.as_view()


@logging.methods_logged(logger, ['setup', 'get', ])
class WatchedIgnoreVolumeView(IgnoreVolumeView):
    redirect_url = 'missing_issues:watched'


watched_ignore_volume_view = WatchedIgnoreVolumeView.as_view()


@logging.methods_logged(logger, ['setup', 'get', ])
class IgnorePublisherView(BaseSkipIgnoreView):
    def process(self):
        self.missing_issue.ignore_publisher()


ignore_publisher_view = IgnorePublisherView.as_view()


@logging.methods_logged(logger, ['setup', 'get', ])
class WatchedIgnorePublisherView(IgnorePublisherView):
    redirect_url = 'missing_issues:watched'


watched_ignore_publisher_view = WatchedIgnorePublisherView.as_view()


@logging.methods_logged(logger, ['get', ])
class IgnoredIssuesListView(IsAdminMixin, ElidedPagesPaginatorMixin, BreadcrumbMixin, ActiveMenuMixin, ListView):
    queryset = IgnoredIssue.objects.all().order_by('publisher_name', 'volume_name', 'volume_start_year', 'number',
                                                   'cover_date', 'comicvine_id')
    breadcrumb = [{'url': reverse_lazy("missing_issues:ignored_issues"), 'text': 'Ignored issues'}]
    active_menu_item = 'ignored_issues'
    template_name = 'missing_issues/ignored_issues_list.html'
    context_object_name = 'ignored_issues'
    paginate_by = 100


ignored_issues_list_view = IgnoredIssuesListView.as_view()


@logging.methods_logged(logger, ['get', ])
class IgnoredVolumesListView(IsAdminMixin, ElidedPagesPaginatorMixin, BreadcrumbMixin, ActiveMenuMixin, ListView):
    queryset = IgnoredVolume.objects.all().order_by('publisher_name', 'name', 'start_year', 'comicvine_id')
    breadcrumb = [{'url': reverse_lazy("missing_issues:ignored_volumes"), 'text': 'Ignored volumes'}]
    active_menu_item = 'ignored_volumes'
    template_name = 'missing_issues/ignored_volumes_list.html'
    context_object_name = 'ignored_volumes'
    paginate_by = 100


ignored_volumes_list_view = IgnoredVolumesListView.as_view()


@logging.methods_logged(logger, ['get', ])
class IgnoredPublishersListView(IsAdminMixin, ElidedPagesPaginatorMixin, BreadcrumbMixin, ActiveMenuMixin, ListView):
    queryset = IgnoredPublisher.objects.all().order_by('name')
    breadcrumb = [{'url': reverse_lazy("missing_issues:ignored_publisher"), 'text': 'Ignored publisher'}]
    active_menu_item = 'ignored_publishers'
    template_name = 'missing_issues/ignored_publishers_list.html'
    context_object_name = 'ignored_publishers'
    paginate_by = 100


ignored_publishers_list_view = IgnoredPublishersListView.as_view()


@logging.methods_logged(logger, ['get', ])
class DeleteView(SingleObjectMixin, View):
    redirect_url = None

    def get(self, request, **kwargs):
        obj = self.get_object()
        obj.delete()
        if request.GET.get('page'):
            return HttpResponseRedirect(reverse_lazy(self.redirect_url) + f"?page={request.GET.get('page')}")
        else:
            return HttpResponseRedirect(reverse_lazy(self.redirect_url))


@logging.methods_logged(logger, ['get', ])
class IgnoredIssueDeleteView(DeleteView):
    redirect_url = "missing_issues:ignored_issues"
    model = IgnoredIssue


ignored_issue_delete_view = IgnoredIssueDeleteView.as_view()


@logging.methods_logged(logger, ['get', ])
class IgnoredVolumeDeleteView(DeleteView):
    redirect_url = "missing_issues:ignored_volumes"
    model = IgnoredVolume


ignored_volume_delete_view = IgnoredVolumeDeleteView.as_view()


@logging.methods_logged(logger, ['get', ])
class IgnoredPublisherDeleteView(DeleteView):
    redirect_url = "missing_issues:ignored_publisher"
    model = IgnoredPublisher


ignored_publisher_delete_view = IgnoredPublisherDeleteView.as_view()


class BaseStartWatchView(SingleObjectMixin, View):
    MISSING_ISSUES_TASK = None

    def get(self, request, **kwargs):
        obj = self.get_object()
        try:
            obj.watchers.create(user=self.request.user)
            task = signature(self.MISSING_ISSUES_TASK, kwargs={'pk': obj.pk})
            task.delay()
            notifications.success(self.request, f"You now watching {obj}")
        except IntegrityError:
            notifications.error(self.request, f"You already watching {obj}")
        return HttpResponseRedirect(obj.get_absolute_url())


class BaseStopWatchView(SingleObjectMixin, View):
    def get(self, request, **kwargs):
        obj = self.get_object()
        try:
            w = obj.watchers.get(user=self.request.user)
            obj.watchers.remove(w)
            notifications.success(self.request, f"You stopped watching {obj}")
        except WatchedItem.DoesNotExist:
            notifications.error(self.request, f"You are not watching {obj}")
        return HttpResponseRedirect(obj.get_absolute_url())


class StartReloadFromDOView(View):
    def get(self, request, **kwargs):
        try:
            publishers_space_task.delay(prefix='comics/')
            notifications.success(self.request, "Refresh from DO started")
        except Exception:
            notifications.error(self.request, "Could not start refresh from DO, please check logs")
        return HttpResponseRedirect(request.GET.get("next", reverse_lazy("missing_issues:all")))


start_reload_from_do_view = StartReloadFromDOView.as_view()
