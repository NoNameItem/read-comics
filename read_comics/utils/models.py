import datetime
import random
import re
from json import JSONDecodeError
from time import sleep

import pytz
import requests
from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.exceptions import FieldDoesNotExist
from django.db import models, transaction
from django.utils import timezone
from pymongo import MongoClient
from requests import HTTPError, RequestException
from requests.adapters import HTTPAdapter
from slugify import slugify
from urllib3 import Retry

from read_comics.missing_issues.models import APIQueue, Locks

from .logging import Logger
from .model_managers import ComicvineSyncManager

default_logger = get_task_logger("comicvine-sync")


def slugify_function(content):
    return slugify(str(content), lowercase=False)


class ComicvineSyncModelConfigurationError(Exception):
    pass


class ComicvineSyncModel(models.Model):
    MONGO_COLLECTION = ""
    MONGO_PROJECTION = {}
    _DEFAULT_FIELDS_MAPPING = {
        "name": "name",
        "aliases": "aliases",
        "short_description": "deck",
        "html_description": {"path": "description", "method": "strip_links"},
        "thumb_url": "image.small_url",
        "image_url": "image.original_url",
        "first_issue_name": {"path": "first_appeared_in_issue.id", "method": "get_issue_name"},
        "first_issue": {"path": "first_appeared_in_issue.id", "method": "get_issue"},
        "first_issue_comicvine_id": "first_appeared_in_issue.id",
    }
    COMICVINE_INFO_TASK = None
    COMICVINE_API_URL = None
    COMICVINE_FORCE_DETAIL_INFO = False

    class ComicvineStatus(models.TextChoices):
        NOT_MATCHED = "NOT_MATCHED", "Not matched"
        QUEUED = "QUEUED", "Waiting in queue"
        MATCHED = "MATCHED", "Matched"

    logger: Logger = default_logger

    comicvine_id = models.IntegerField(unique=True)
    comicvine_url = models.URLField(max_length=1000, null=True)
    comicvine_status = models.CharField(
        max_length=15, choices=ComicvineStatus.choices, default=ComicvineStatus.NOT_MATCHED
    )
    comicvine_last_match = models.DateTimeField(null=True)

    created_dt = models.DateTimeField(auto_now_add=True)
    modified_dt = models.DateTimeField(auto_now_add=True)

    objects = ComicvineSyncManager()

    class Meta:
        abstract = True

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self} ({self.pk})>"

    @property
    def comicvine_actual(self):
        if self.comicvine_status != self.ComicvineStatus.MATCHED:
            return False
        document = self.comicvine_document
        if document:
            self.logger.info(f"Document with id `{self.comicvine_id}` found in collection `{self.MONGO_COLLECTION}`")
            self.logger.debug(f"Document: {str(document)}")
            crawl_date = document["crawl_date"]
            return self.comicvine_last_match > pytz.UTC.localize(crawl_date)
        else:
            self.logger.warning(
                f"Document with id `{self.comicvine_id}` not found in collection `{self.MONGO_COLLECTION}`"
            )
            return True

    @property
    def comicvine_document(self):
        client = MongoClient(settings.MONGO_URL)
        db = client.get_default_database()
        collection = db[self.MONGO_COLLECTION]
        client.close()
        return collection.find_one({"id": self.comicvine_id}, self.MONGO_PROJECTION)

    def pre_save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        pass

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.pre_save(force_insert, force_update, using, update_fields)
        if self.tracker.changed():
            self.logger.debug("Changes detected, updating modified_dt")
            self.modified_dt = timezone.now()
        super(ComicvineSyncModel, self).save(force_insert, force_update, using, update_fields)
        self.post_save()

    def get_document_from_api(self):
        retries = Retry(total=100, backoff_factor=300, status_forcelist=[500, 502, 503, 504, 522, 524, 408, 429, 420])
        adapter = HTTPAdapter(max_retries=retries)
        http = requests.Session()
        http.mount("https://", adapter)
        http.mount("http://", adapter)
        url = self.COMICVINE_API_URL.format(id=self.comicvine_id, api_key=random.choice(settings.COMICVINE_API_KEYS))
        headers = {"user-agent": "read-comics.net/1.0.0"}
        try:
            response = http.request("GET", url, headers=headers, timeout=100)
            response.raise_for_status()
            d = response.json().get("results", {})
            if d:
                client = MongoClient(settings.MONGO_URL)
                db = client.get_default_database()
                d["crawl_date"] = timezone.now()
                d["crawl_source"] = "detail"
                collection = db[self.MONGO_COLLECTION]
                collection.replace_one({"id": d["id"]}, d, upsert=True)
                document = collection.find_one({"id": self.comicvine_id}, self.MONGO_PROJECTION)
                client.close()
                return document  # noqa R504
            else:
                return None
        except (JSONDecodeError, RequestException, HTTPError):
            return None

    def fill_from_comicvine(self, follow_m2m=True, delay=False, force_api_refresh=False):
        if delay:
            if self.COMICVINE_INFO_TASK:
                # self.COMICVINE_INFO_TASK.delay(pk=self.pk, follow_m2m=follow_m2m)
                self.COMICVINE_INFO_TASK.apply_async(
                    (),
                    {
                        "pk": self.pk,
                        "follow_m2m": follow_m2m,
                        "force_api_refresh": force_api_refresh,
                    },
                    priority=1,
                )
                self.comicvine_status = self.ComicvineStatus.QUEUED
            return

        document = self.comicvine_document
        document_source = document.get("crawl_source", "list") if document else "list"
        if document and not force_api_refresh and (document_source == "detail" or not self.COMICVINE_FORCE_DETAIL_INFO):
            self.logger.info(f"Document with id `{self.comicvine_id}` found in collection `{self.MONGO_COLLECTION}`")
            self.logger.debug(f"Document: {str(document)}")
            self.process_document(document, follow_m2m)
            self.comicvine_status = self.ComicvineStatus.MATCHED
            self.comicvine_last_match = timezone.now()
        else:
            if force_api_refresh:
                self.logger.info(
                    f"Forced API refresh for document with id `{self.comicvine_id}` "
                    f"in collection `{self.MONGO_COLLECTION}`"
                )
            else:
                self.logger.warning(
                    f"Document with id `{self.comicvine_id}` not found in collection `{self.MONGO_COLLECTION}`"
                )

            with transaction.atomic():
                task_queue = APIQueue(endpoint=self.MONGO_COLLECTION, comicvine_id=self.comicvine_id)
                task_queue.save()

            sleep(1)
            try:
                task_queue = APIQueue.objects.get(id=task_queue.id)
            except APIQueue.DoesNotExist:
                task_queue = None
            queue_try_count = 1
            queue_wait_start_dttm = timezone.now()
            while True:
                with transaction.atomic():
                    queue_position = (
                        APIQueue.objects.filter(
                            added_in_queue__lt=task_queue.added_in_queue,
                            endpoint=self.MONGO_COLLECTION,
                        ).count()
                        if task_queue
                        else 0
                    )
                    if queue_position > 0:
                        self.logger.info(
                            f"Waiting API queue for `{self.comicvine_id}` in `{self.MONGO_COLLECTION}` "
                            f"(Try: {queue_try_count} "
                            f"waiting for {timezone.now() - queue_wait_start_dttm})"
                        )
                        queue_try_count += 1
                        sleep(settings.COMICVINE_API_DELAY * queue_position)
                        continue
                    else:
                        self.logger.info(
                            f"Finished waiting API queue for `{self.comicvine_id}` in `{self.MONGO_COLLECTION}` "
                            f"(Try: {queue_try_count} "
                            f"waited for {timezone.now() - queue_wait_start_dttm})"
                        )
                        break

            api_try_count = 1
            api_wait_start_dttm = timezone.now()
            while True:
                with transaction.atomic():
                    now = timezone.now()
                    lock = Locks.objects.select_for_update().filter(code=self.MONGO_COLLECTION)[0]
                    if lock.dttm is None or now - lock.dttm > datetime.timedelta(seconds=settings.COMICVINE_API_DELAY):
                        self.logger.info(
                            f"Finished waiting API for `{self.comicvine_id}` in"
                            f" `{self.MONGO_COLLECTION}` (Try: {api_try_count}, "
                            f"waited for {timezone.now() - api_wait_start_dttm})"
                        )
                        document = self.get_document_from_api()
                        lock.dttm = timezone.now()
                        lock.save()
                        if task_queue:
                            task_queue.delete()
                        break
                    else:
                        self.logger.info(
                            f"Waiting API for `{self.comicvine_id}` in `{self.MONGO_COLLECTION}` (Try: {api_try_count} "
                            f"waiting for {timezone.now() - api_wait_start_dttm})"
                        )
                        api_try_count += 1
                        sleep(1)

            if document:
                self.logger.info(f"Document with id `{self.comicvine_id}` found in API (`{self.MONGO_COLLECTION}`)")
                self.logger.debug(f"Document: {str(document)}")
                self.process_document(document, follow_m2m)
                self.comicvine_status = self.ComicvineStatus.MATCHED
                self.comicvine_last_match = timezone.now()
            else:
                self.logger.error(
                    f"Document with id `{self.comicvine_id}` not found in API (`{self.MONGO_COLLECTION}`)"
                )
                self.comicvine_status = self.ComicvineStatus.NOT_MATCHED

    def process_document(self, document, follow_m2m):
        self.comicvine_url = document.get("site_detail_url")
        field_mapping = self.get_field_mapping()
        for field, source in field_mapping.items():
            self._fill_field_from_document(document, field, source, follow_m2m)

    def get_field_mapping(self):
        field_mapping = dict(self._DEFAULT_FIELDS_MAPPING)
        if hasattr(self, "FIELD_MAPPING"):
            field_mapping.update(self.FIELD_MAPPING)
        return field_mapping

    @staticmethod
    def strip_links(text):
        if text:
            return re.sub(r"<(a|/a).*?>", "", text)
        return None

    @staticmethod
    def get_issue_name(comicvine_id):
        try:
            client = MongoClient(settings.MONGO_URL)
            db = client.get_default_database()
            issue_doc = db["comicvine_issues"].find_one({"id": comicvine_id})
            if issue_doc:
                volume_doc = db["comicvine_volumes"].find_one({"id": issue_doc["volume"]["id"]})
                if volume_doc:
                    if issue_doc["name"]:
                        issue_name = issue_doc["name"]
                    else:
                        issue_name = ""
                    name = (
                        f"{volume_doc['name']} ({volume_doc['start_year']}) "
                        f"#{issue_doc['issue_number']} {issue_name}"
                    )
                    client.close()
                    return name.strip(" ")
            client.close()
            return ""
        except KeyError:
            return ""

    @staticmethod
    def get_issue(comicvine_id):
        from read_comics.issues.models import Issue

        try:
            return Issue.objects.get(comicvine_id=comicvine_id)
        except Issue.DoesNotExist:
            return None

    @staticmethod
    def get_character(d):
        if not d:
            return None
        comicvine_id = d.get("id", None)
        name = d.get("name", str(comicvine_id))
        if not comicvine_id:
            return None
        from read_comics.characters.models import Character

        character, created, matched = Character.objects.get_or_create_from_comicvine(
            comicvine_id, defaults={"name": name}, delay=True
        )
        return character

    @staticmethod
    def get_concept(d):
        if not d:
            return None
        comicvine_id = d.get("id", None)
        name = d.get("name", str(comicvine_id))
        if not comicvine_id:
            return None
        from read_comics.concepts.models import Concept

        concept, created, matched = Concept.objects.get_or_create_from_comicvine(
            comicvine_id, defaults={"name": name}, delay=True
        )
        return concept

    @staticmethod
    def get_location(d):
        if not d:
            return None
        comicvine_id = d.get("id", None)
        name = d.get("name", str(comicvine_id))
        if not comicvine_id:
            return None
        from read_comics.locations.models import Location

        location, created, matched = Location.objects.get_or_create_from_comicvine(
            comicvine_id, defaults={"name": name}, delay=True
        )
        return location

    @staticmethod
    def get_object(d):
        if not d:
            return None
        comicvine_id = d.get("id", None)
        name = d.get("name", str(comicvine_id))
        if not comicvine_id:
            return None
        from read_comics.objects.models import Object

        obj, created, matched = Object.objects.get_or_create_from_comicvine(
            comicvine_id, defaults={"name": name}, delay=True
        )
        return obj

    @staticmethod
    def get_power(d):
        if not d:
            return None
        comicvine_id = d.get("id", None)
        name = d.get("name", str(comicvine_id))
        if not comicvine_id:
            return None
        from read_comics.powers.models import Power

        power, created, matched = Power.objects.get_or_create_from_comicvine(
            comicvine_id, defaults={"name": name}, delay=True
        )
        return power

    @staticmethod
    def get_story_arc(d):
        if not d:
            return None
        comicvine_id = d.get("id", None)
        name = d.get("name", str(comicvine_id))
        if not comicvine_id:
            return None
        from read_comics.story_arcs.models import StoryArc

        story_arc, created, matched = StoryArc.objects.get_or_create_from_comicvine(
            comicvine_id, defaults={"name": name}, delay=True
        )
        return story_arc

    @staticmethod
    def get_team(d):
        if not d:
            return None
        comicvine_id = d.get("id", None)
        name = d.get("name", str(comicvine_id))
        if not comicvine_id:
            return None
        from read_comics.teams.models import Team

        team, created, matched = Team.objects.get_or_create_from_comicvine(
            comicvine_id, defaults={"name": name}, delay=True
        )
        return team

    @staticmethod
    def get_volume(d):
        if not d:
            return None
        comicvine_id = d.get("id", None)
        name = d.get("name", str(comicvine_id))
        if not comicvine_id:
            return None
        from read_comics.volumes.models import Volume

        volume, created, matched = Volume.objects.get_or_create_from_comicvine(
            comicvine_id, defaults={"name": name}, delay=False
        )
        return volume

    @staticmethod
    def get_publisher(d):
        if not d:
            return None
        comicvine_id = d.get("id", None)
        name = d.get("name", str(comicvine_id))
        if not comicvine_id:
            return None
        from read_comics.publishers.models import Publisher

        publisher, created, matched = Publisher.objects.get_or_create_from_comicvine(
            comicvine_id, defaults={"name": name}, delay=False
        )
        return publisher

    @staticmethod
    def get_person(d):
        if not d:
            return None
        comicvine_id = d.get("id", None)
        name = d.get("name", str(comicvine_id))
        if not comicvine_id:
            return None
        from read_comics.people.models import Person

        person, created, matched = Person.objects.get_or_create_from_comicvine(
            comicvine_id, defaults={"name": name}, delay=True
        )
        return person

    def _fill_field_from_document(self, document, field, source, follow_m2m):
        if not hasattr(self, field):
            return

        if not isinstance(source, (str, dict)):
            raise ComicvineSyncModelConfigurationError("Wrong document source")

        if isinstance(source, str):
            path = source
            method = None
            inner_path = ""
            override_m2m = True
        elif isinstance(source, dict):
            path = source.get("path", "")
            method = getattr(self, source.get("method"), None)
            if not method or not callable(method):
                raise ComicvineSyncModelConfigurationError(f"Wrong method `{source.get('method')}`")
            inner_path = source.get("inner_path", "")
            override_m2m = source.get("overrride_m2m", True)

        try:
            model_field = self._meta.get_field(field)
            if isinstance(model_field, models.ManyToManyField):
                if follow_m2m:
                    self._set_m2m_from_document(document, field, path, inner_path, method, override_m2m)

            else:
                self._set_non_m2m_from_document(document, field, method, path)
        except FieldDoesNotExist:
            # If there is no such field, do nothing
            pass

    def _set_non_m2m_from_document(self, document, field, method, path):
        value = self._get_value_by_path(document, path)
        if method:
            try:
                value = method(value)
            except TypeError:
                ComicvineSyncModelConfigurationError("Wrong method")
        setattr(self, field, value)

    def _get_value_by_path(self, document, path):
        value = document
        for path_element in path.split("."):
            if path_element == "":
                return value
            if value is None:
                self.logger.warning(f"Document ended before path ({path}). Comicvine ID: {self.comicvine_id}")
                return None
            if isinstance(value, dict):
                try:
                    value = value[path_element]
                except KeyError:
                    self.logger.warning(f"No such key in document: `{path_element}`. Comicvine ID: {self.comicvine_id}")
                    value = None
            elif isinstance(value, list):
                try:
                    value = value[int(path_element)]
                except (IndexError, ValueError):
                    self.logger.warning(f"No such key in document: `{path_element}`. Comicvine ID: {self.comicvine_id}")
                    value = None
            else:
                value = None
        return value

    def _set_m2m_from_document(self, document, field, path, inner_path, method, override):
        f = getattr(self, field)

        if override:
            f.clear()

        outer_item = self._get_value_by_path(document, path)

        # Convert dict item to list for unification
        if not isinstance(outer_item, list):
            outer_item = [outer_item]

        for inner_document in outer_item:
            if inner_path:
                inner_value = self._get_value_by_path(inner_document, inner_path)
            else:
                inner_value = inner_document
            defaults = {}
            if method:
                value = method(inner_value)
                try:
                    inner_value, defaults = value
                except TypeError:
                    inner_value = value
                    defaults = None
            if inner_value:
                f.add(inner_value, through_defaults=defaults)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.logger:
            self.logger = default_logger

    def post_save(self):
        pass

    @property
    def description(self):
        if self.html_description:
            d = self.html_description  # .replace("https:", "http:")
            from bs4 import BeautifulSoup

            soup = BeautifulSoup(d, "html.parser")
            lazy_images = soup.select("img.js-lazy-load-image")
            for image in lazy_images:
                image["src"] = image.get("data-src")

            images = soup.select("img")
            for image in images:
                classes = image.get("class", [])
                classes.append("image-full-size")
                image["class"] = classes

            return str(soup)
        return ""

    @property
    def meta(self):
        return self._meta

    @property
    def display_name(self):
        return str(self)
