import datetime
import json
from collections import namedtuple
from typing import Any, Callable, List

from celery import signature
from django import http
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Q, QuerySet
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django_magnificent_messages import notifications
from issues.tasks import issue_entry_task, purge_deleted
from pymongo import MongoClient
from utils import logging
from utils.view_mixins import ActiveMenuMixin, BreadcrumbMixin, ElidedPagesPaginatorMixin, IsAdminMixin
from volumes.tasks import volume_entry_task

from read_comics.characters.models import Character
from read_comics.concepts.models import Concept
from read_comics.locations.models import Location
from read_comics.objects.models import Object
from read_comics.people.models import Person
from read_comics.publishers.models import Publisher
from read_comics.publishers.tasks import publisher_entry_task, publishers_space_task
from read_comics.story_arcs.models import StoryArc
from read_comics.teams.models import Team
from read_comics.utils.comicvine_text import numerical_issue_number, set_lazy_image_sources, split_aliases, strip_links
from read_comics.volumes.models import Volume

from .do_spaces import get_level
from .models import IgnoredIssue, IgnoredPublisher, IgnoredVolume, MissingIssue, WatchedItem
from .queries import get_watched_missing_issues_query

logger = logging.getLogger(__name__)

CATEGORY_MODELS = {
    "character": Character,
    "concept": Concept,
    "location": Location,
    "object": Object,
    "person": Person,
    "publisher": Publisher,
    "story_arc": StoryArc,
    "team": Team,
    "volume": Volume,
}


@logging.methods_logged(
    logger,
    [
        "setup",
        "get",
    ],
)
class MissingIssuesListView(IsAdminMixin, ElidedPagesPaginatorMixin, BreadcrumbMixin, ActiveMenuMixin, ListView):
    template_name = "missing_issues/missing_issues_list.html"
    template_name_partial = "missing_issues/issues_table.html"
    active_menu_item = "missing_issues"
    context_object_name = "missing_issues"
    paginate_by = 100
    category_skip_publisher_url = "missing_issues:category_skip_publisher"
    category_ignore_publisher_url = "missing_issues:category_ignore_publisher"
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

    breadcrumb = [{"url": reverse_lazy("missing_issues:all"), "text": "Missing issues"}]

    def __init__(self, **kwargs: Any):
        super(MissingIssuesListView, self).__init__(**kwargs)
        self.category_key = None
        self.slug = None
        self.obj = None

    def setup(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> None:
        super(MissingIssuesListView, self).setup(request, *args, **kwargs)
        self.category_key = kwargs.get("category", None)
        self.slug = kwargs.get("slug", None)

        if self.category_key:
            try:
                self.obj = CATEGORY_MODELS[self.category_key].objects.get(slug=self.slug)
            except (KeyError, ObjectDoesNotExist):
                raise Http404

    def get_queryset(self) -> QuerySet:
        if self.obj:
            q = self.obj.missing_issues.filter(skip=False).order_by(
                "publisher_name",
                "publisher_comicvine_id",
                "volume_name",
                "volume_start_year",
                "volume_comicvine_id",
                "numerical_number",
                "number",
                "comicvine_id",
            )
        else:
            q = MissingIssue.objects.filter(skip=False).order_by(
                "publisher_name",
                "publisher_comicvine_id",
                "volume_name",
                "volume_start_year",
                "volume_comicvine_id",
                "numerical_number",
                "number",
                "comicvine_id",
            )

        search_query = self.request.GET.get("q")

        if search_query:
            q = q.filter(
                Q(publisher_name__icontains=search_query)
                | Q(volume_name__icontains=search_query)
                | Q(name__icontains=search_query)
            )

        return q.order_by(
            "publisher_name",
            "publisher_comicvine_id",
            "volume_name",
            "volume_start_year",
            "volume_comicvine_id",
            "numerical_number",
            "number",
            "comicvine_id",
        )

    def get_breadcrumb(self):
        if self.obj:
            return self.breadcrumb + [{"url": "", "text": str(self.obj)}]
        return self.breadcrumb

    def get_template_names(self) -> List[str]:
        response_type = self.request.GET.get("response_type")
        if response_type == "partial":
            return [self.template_name_partial]
        return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super(MissingIssuesListView, self).get_context_data(**kwargs)
        context["obj"] = self.obj
        context["category_key"] = self.category_key
        context["urls"] = {
            "category_skip_publisher": self.category_skip_publisher_url,
            "category_ignore_publisher": self.category_ignore_publisher_url,
            "category_skip_volume": self.category_skip_volume_url,
            "category_ignore_volume": self.category_ignore_volume_url,
            "category_skip_issue": self.category_skip_issue_url,
            "category_ignore_issue": self.category_ignore_issue_url,
            "skip_publisher": self.skip_publisher_url,
            "ignore_publisher": self.ignore_publisher_url,
            "skip_volume": self.skip_volume_url,
            "ignore_volume": self.ignore_volume_url,
            "skip_issue": self.skip_issue_url,
            "ignore_issue": self.ignore_issue_url,
        }
        context["q"] = self.request.GET.get("q")
        return context


missing_issues_list_view = MissingIssuesListView.as_view()


@logging.methods_logged(
    logger,
    [
        "setup",
        "get",
    ],
)
class WatchedMissingIssuesListView(MissingIssuesListView):
    skip_publisher_url = "missing_issues:watched_skip_publisher"
    ignore_publisher_url = "missing_issues:watched_ignore_publisher"
    skip_volume_url = "missing_issues:watched_skip_volume"
    ignore_volume_url = "missing_issues:watched_ignore_volume"
    skip_issue_url = "missing_issues:watched_skip_issue"
    ignore_issue_url = "missing_issues:watched_ignore_issue"

    breadcrumb = [{"url": reverse_lazy("missing_issues:watched"), "text": "Watched missing issues"}]

    def get_queryset(self) -> QuerySet:
        search_query = self.request.GET.get("q")

        return get_watched_missing_issues_query(self.request.user, search_query).order_by(
            "publisher_name",
            "publisher_comicvine_id",
            "volume_name",
            "volume_start_year",
            "volume_comicvine_id",
            "numerical_number",
            "number",
            "comicvine_id",
        )


watched_missing_issues_list_view = WatchedMissingIssuesListView.as_view()


class BaseSkipIgnoreView(IsAdminMixin, View):
    category_redirect_url = "missing_issues:category"
    redirect_url = "missing_issues:all"

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
        self.category_key = kwargs.get("category", None)
        self.slug = kwargs.get("slug", None)
        self.missing_issue_comicvine_id = kwargs.get("comicvine_id")

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
            return JsonResponse(status=404, data={"message": "Object not found"})
        elif self.missing_issue_not_found:
            return JsonResponse(
                status=404,
                data={
                    "message": f"Missing issue with comicvine_id = {self.missing_issue_comicvine_id} "
                    f'not found, may be it"s already processed'
                },
            )
        else:
            try:
                self.process()

            except Exception as err:
                logger.error(err)
                return JsonResponse(status=500, data={"message": "Error occurred. Please check logs"})

        if self.obj:
            url = reverse_lazy(
                self.category_redirect_url, kwargs={"category": self.category_key, "slug": self.obj.slug}
            )
        else:
            url = reverse_lazy(self.redirect_url)

        if request.GET.get("page"):
            url = url + f"?page={request.GET.get('page')}&response_type=partial"
        else:
            url = url + "?response_type=partial"

        if request.GET.get("q"):
            url += f"&q={request.GET.get('q')}"

        return HttpResponseRedirect(url)

    def process(self):
        raise NotImplementedError


@logging.methods_logged(
    logger,
    [
        "setup",
        "get",
    ],
)
class SkipIssueView(BaseSkipIgnoreView):
    def process(self):
        self.missing_issue.skip = True
        self.missing_issue.skip_date = datetime.date.today()
        self.missing_issue.save()


skip_issue_view = SkipIssueView.as_view()


@logging.methods_logged(
    logger,
    [
        "setup",
        "get",
    ],
)
class WatchedSkipIssueView(SkipIssueView):
    redirect_url = "missing_issues:watched"


watched_skip_issue_view = WatchedSkipIssueView.as_view()


@logging.methods_logged(
    logger,
    [
        "setup",
        "get",
    ],
)
class SkipVolumeView(BaseSkipIgnoreView):
    def process(self):
        MissingIssue.objects.filter(volume_comicvine_id=self.missing_issue.volume_comicvine_id).update(
            skip=True, skip_date=datetime.date.today()
        )


skip_volume_view = SkipVolumeView.as_view()


@logging.methods_logged(
    logger,
    [
        "setup",
        "get",
    ],
)
class WatchedSkipVolumeView(SkipVolumeView):
    redirect_url = "missing_issues:watched"


watched_skip_volume_view = WatchedSkipVolumeView.as_view()


@logging.methods_logged(
    logger,
    [
        "setup",
        "get",
    ],
)
class SkipPublisherView(BaseSkipIgnoreView):
    def process(self):
        MissingIssue.objects.filter(publisher_comicvine_id=self.missing_issue.publisher_comicvine_id).update(
            skip=True, skip_date=datetime.date.today()
        )


skip_publisher_view = SkipPublisherView.as_view()


@logging.methods_logged(
    logger,
    [
        "setup",
        "get",
    ],
)
class WatchedSkipPublisherView(SkipPublisherView):
    redirect_url = "missing_issues:watched"


watched_skip_publisher_view = WatchedSkipPublisherView.as_view()


@logging.methods_logged(
    logger,
    [
        "setup",
        "get",
    ],
)
class IgnoreIssueView(BaseSkipIgnoreView):
    def process(self):
        self.missing_issue.ignore()


ignore_issue_view = IgnoreIssueView.as_view()


@logging.methods_logged(
    logger,
    [
        "setup",
        "get",
    ],
)
class WatchedIgnoreIssueView(IgnoreIssueView):
    redirect_url = "missing_issues:watched"


watched_ignore_issue_view = WatchedIgnoreIssueView.as_view()


@logging.methods_logged(
    logger,
    [
        "setup",
        "get",
    ],
)
class IgnoreVolumeView(BaseSkipIgnoreView):
    def process(self):
        self.missing_issue.ignore_volume()


ignore_volume_view = IgnoreVolumeView.as_view()


@logging.methods_logged(
    logger,
    [
        "setup",
        "get",
    ],
)
class WatchedIgnoreVolumeView(IgnoreVolumeView):
    redirect_url = "missing_issues:watched"


watched_ignore_volume_view = WatchedIgnoreVolumeView.as_view()


@logging.methods_logged(
    logger,
    [
        "setup",
        "get",
    ],
)
class IgnorePublisherView(BaseSkipIgnoreView):
    def process(self):
        self.missing_issue.ignore_publisher()


ignore_publisher_view = IgnorePublisherView.as_view()


@logging.methods_logged(
    logger,
    [
        "setup",
        "get",
    ],
)
class WatchedIgnorePublisherView(IgnorePublisherView):
    redirect_url = "missing_issues:watched"


watched_ignore_publisher_view = WatchedIgnorePublisherView.as_view()


@logging.methods_logged(
    logger,
    [
        "get",
    ],
)
class IgnoredIssuesListView(IsAdminMixin, ElidedPagesPaginatorMixin, BreadcrumbMixin, ActiveMenuMixin, ListView):
    queryset = IgnoredIssue.objects.all().order_by(
        "publisher_name", "volume_name", "volume_start_year", "number", "cover_date", "comicvine_id"
    )
    breadcrumb = [{"url": reverse_lazy("missing_issues:ignored_issues"), "text": "Ignored issues"}]
    active_menu_item = "ignored_issues"
    template_name = "missing_issues/ignored_issues_list.html"
    context_object_name = "ignored_issues"
    paginate_by = 100


ignored_issues_list_view = IgnoredIssuesListView.as_view()


@logging.methods_logged(
    logger,
    [
        "get",
    ],
)
class IgnoredVolumesListView(IsAdminMixin, ElidedPagesPaginatorMixin, BreadcrumbMixin, ActiveMenuMixin, ListView):
    queryset = IgnoredVolume.objects.all().order_by("publisher_name", "name", "start_year", "comicvine_id")
    breadcrumb = [{"url": reverse_lazy("missing_issues:ignored_volumes"), "text": "Ignored volumes"}]
    active_menu_item = "ignored_volumes"
    template_name = "missing_issues/ignored_volumes_list.html"
    context_object_name = "ignored_volumes"
    paginate_by = 100


ignored_volumes_list_view = IgnoredVolumesListView.as_view()


@logging.methods_logged(
    logger,
    [
        "get",
    ],
)
class IgnoredPublishersListView(IsAdminMixin, ElidedPagesPaginatorMixin, BreadcrumbMixin, ActiveMenuMixin, ListView):
    queryset = IgnoredPublisher.objects.all().order_by("name")
    breadcrumb = [{"url": reverse_lazy("missing_issues:ignored_publisher"), "text": "Ignored publisher"}]
    active_menu_item = "ignored_publishers"
    template_name = "missing_issues/ignored_publishers_list.html"
    context_object_name = "ignored_publishers"
    paginate_by = 100


ignored_publishers_list_view = IgnoredPublishersListView.as_view()


@logging.methods_logged(
    logger,
    [
        "get",
    ],
)
class DeleteView(SingleObjectMixin, View):
    redirect_url = None

    def get(self, request, **kwargs):
        obj = self.get_object()
        obj.delete()
        if request.GET.get("page"):
            return HttpResponseRedirect(reverse_lazy(self.redirect_url) + f"?page={request.GET.get('page')}")
        else:
            return HttpResponseRedirect(reverse_lazy(self.redirect_url))


@logging.methods_logged(
    logger,
    [
        "get",
    ],
)
class IgnoredIssueDeleteView(IsAdminMixin, DeleteView):
    redirect_url = "missing_issues:ignored_issues"
    model = IgnoredIssue


ignored_issue_delete_view = IgnoredIssueDeleteView.as_view()


@logging.methods_logged(
    logger,
    [
        "get",
    ],
)
class IgnoredVolumeDeleteView(IsAdminMixin, DeleteView):
    redirect_url = "missing_issues:ignored_volumes"
    model = IgnoredVolume


ignored_volume_delete_view = IgnoredVolumeDeleteView.as_view()


@logging.methods_logged(
    logger,
    [
        "get",
    ],
)
class IgnoredPublisherDeleteView(IsAdminMixin, DeleteView):
    redirect_url = "missing_issues:ignored_publisher"
    model = IgnoredPublisher


ignored_publisher_delete_view = IgnoredPublisherDeleteView.as_view()


class BaseStartWatchView(IsAdminMixin, SingleObjectMixin, View):
    MISSING_ISSUES_TASK = None

    def get(self, request, **kwargs):
        obj = self.get_object()
        try:
            obj.watchers.create(user=self.request.user)
            task = signature(self.MISSING_ISSUES_TASK, kwargs={"pk": obj.pk})
            task.delay()
            notifications.success(self.request, f"You now watching {obj}")
        except IntegrityError:
            notifications.error(self.request, f"You already watching {obj}")
        return HttpResponseRedirect(obj.get_absolute_url())


class BaseStopWatchView(IsAdminMixin, SingleObjectMixin, View):
    def get(self, request, **kwargs):
        obj = self.get_object()
        try:
            w = obj.watchers.get(user=self.request.user)
            obj.watchers.remove(w)
            notifications.success(self.request, f"You stopped watching {obj}")
        except WatchedItem.DoesNotExist:
            notifications.error(self.request, f"You are not watching {obj}")
        return HttpResponseRedirect(obj.get_absolute_url())


class StartReloadFromDOView(IsAdminMixin, View):
    LEVEL_TO_TASK_MAPPING = {
        1: publishers_space_task,
        2: publisher_entry_task,
        3: volume_entry_task,
        4: issue_entry_task,
    }

    LEVEL_KWARGS = {1: "prefix"}

    def start_task(self, level, key, size):
        kwarg_name = self.LEVEL_KWARGS.get(level, "key")
        task = self.LEVEL_TO_TASK_MAPPING[level]
        kwargs = {kwarg_name: key, "size": size}
        task.delay(**kwargs)

    def post(self, request, **kwargs):
        try:
            body_unicode = request.body.decode("utf-8")
            selected_nodes = json.loads(body_unicode)["data"]
            for node in selected_nodes:
                self.start_task(node["level"], node["key"], node["size"])

            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "error": str(e)})


start_reload_from_do_view = StartReloadFromDOView.as_view()


class PurgeDeletedFromDOView(IsAdminMixin, View):
    def post(self, request, **kwargs):
        try:
            purge_deleted.delay()
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "error": str(e)})


purge_deleted_from_do_view = PurgeDeletedFromDOView.as_view()


class DOSpaceView(IsAdminMixin, View):
    def get(self, request, **kwargs):
        prefix = self.request.GET.get("prefix", "")

        objects = get_level(prefix)

        data = []
        for obj in objects:
            node = {"text": obj["name"], "full_name": obj["full_name"], "size": obj["size"]}

            if obj["name"].lower().endswith(".cbr") or obj["name"].lower().endswith(".cbz"):
                node["children"] = []
                node["icon"] = False
                node["children_link"] = ""
            else:
                node["children"] = True
                node["children_link"] = f"{reverse_lazy('missing_issues:do_space')}?prefix={obj['full_name']}"

            data.append(node)

        return JsonResponse(data, safe=False)


do_space_view = DOSpaceView.as_view()


@logging.methods_logged(logger, ["setup", "get"])
class ComicvineDetailsView(IsAdminMixin, View):
    Field = namedtuple("Field", "state value")

    PUBLISHERS_COLLECTION = "comicvine_publishers"
    VOLUMES_COLLECTION = "comicvine_volumes"
    ISSUES_COLLECTION = "comicvine_issues"

    PUBLISHER_PROJECTION = {
        "_id": 0,
        "id": 1,
        "name": 1,
        "aliases": 1,
        "deck": 1,
        "description": 1,
        "site_detail_url": 1,
        "crawl_date": 1,
        "crawl_source": 1,
    }

    VOLUME_PROJECTION = {
        "_id": 0,
        "id": 1,
        "name": 1,
        "start_year": 1,
        "publisher": 1,
        "first_issue": 1,
        "last_issue": 1,
        "aliases": 1,
        "deck": 1,
        "description": 1,
        "site_detail_url": 1,
        "crawl_date": 1,
        "crawl_source": 1,
    }
    VOLUME_ISSUES_PROJECTION = {
        "_id": 0,
        "id": 1,
        "issue_number": 1,
        "cover_date": 1,
        "image.small_url": 1,
        "image.original_url": 1,
    }

    # image_url is the displayed picture, full_url is the original opened on click; both None without an image
    Cover = namedtuple("Cover", "number cover_date image_url full_url")

    # level -> (collection attribute, projection, context method); later levels only add entries
    LEVELS = {
        "publisher": ("PUBLISHERS_COLLECTION", PUBLISHER_PROJECTION, "publisher_context"),
        "volume": ("VOLUMES_COLLECTION", VOLUME_PROJECTION, "volume_context"),
    }

    @staticmethod
    def make_field(doc: dict, key: str, transform: Callable | None = None) -> "ComicvineDetailsView.Field":
        Field = ComicvineDetailsView.Field
        if key not in doc:
            return Field("missing", None)
        value = doc[key]
        if value in (None, "", []):
            return Field("empty", None)
        if transform is not None:
            value = transform(value)
            if not value:
                return Field("empty", None)
        return Field("value", value)

    @staticmethod
    def cover_sort_key(issue: dict) -> tuple:
        number = numerical_issue_number(issue.get("issue_number"))
        return (number is None, number or 0, issue.get("issue_number") or "", issue["id"])

    @classmethod
    def text_fields(cls, doc: dict) -> dict:
        """Aliases, deck and description: shared by the publisher and the volume."""
        return {
            "aliases": cls.make_field(doc, "aliases", split_aliases),
            "deck": cls.make_field(doc, "deck"),
            "description": cls.make_field(doc, "description", lambda text: set_lazy_image_sources(strip_links(text))),
        }

    def publisher_context(self, db, doc: dict) -> dict:
        return {"title": doc.get("name") or f"Publisher {doc['id']}", "fields": self.text_fields(doc)}

    def volume_context(self, db, doc: dict) -> dict:
        make_field = self.make_field

        def issue_label(issue: dict) -> str | None:
            number = issue.get("issue_number")
            return f"#{number}" if number else None

        issues = sorted(
            db[self.ISSUES_COLLECTION].find({"volume.id": doc["id"]}, self.VOLUME_ISSUES_PROJECTION),
            key=self.cover_sort_key,
        )
        covers = []
        for issue in issues:
            image = issue.get("image") or {}
            number, cover_date = issue.get("issue_number"), issue.get("cover_date")
            covers.append(self.Cover(number, cover_date, image.get("small_url"), image.get("original_url")))

        name = doc.get("name") or f"Volume {doc['id']}"
        start_year = doc.get("start_year")
        return {
            "title": f"{name} ({start_year})" if start_year else name,
            "fields": {
                "year": make_field(doc, "start_year"),
                "publisher": make_field(doc, "publisher", lambda publisher: publisher.get("name")),
                "first_issue": make_field(doc, "first_issue", issue_label),
                "last_issue": make_field(doc, "last_issue", issue_label),
                **self.text_fields(doc),
            },
            "covers": covers,
            "issues_count": len(covers),
        }

    def get(self, request, level: str, comicvine_id: int, **kwargs):
        if level not in self.LEVELS:
            raise Http404
        collection_attr, projection, context_method = self.LEVELS[level]

        client = MongoClient(settings.MONGO_URL)
        try:
            db = client.get_default_database()
            doc = db[getattr(self, collection_attr)].find_one({"id": comicvine_id}, projection)
            if doc is None:
                return render(
                    request, "missing_issues/comicvine/no_data.html", {"level": level, "comicvine_id": comicvine_id}
                )
            context = getattr(self, context_method)(db, doc)
        finally:
            client.close()

        context.update(
            site_detail_url=doc.get("site_detail_url"),
            crawl_date=doc.get("crawl_date"),
            list_only=doc.get("crawl_source") == "list",
        )
        return render(request, f"missing_issues/comicvine/{level}.html", context)


comicvine_details_view = ComicvineDetailsView.as_view()
