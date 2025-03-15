import re

import boto3
import pytz
from celery import Task, shared_task, signature
from celery.utils.log import get_task_logger
from django.apps import apps
from django.conf import settings
from django.db import DatabaseError, OperationalError
from pymongo import MongoClient
from scrapy.settings import Settings

import read_comics.spiders.settings as spiders_settings_file
from read_comics.spiders.scrappyscript import Job, Processor
from read_comics.spiders.spiders.full_spider import FullSpider


class WrongKeyFormatError(Exception):
    pass


class BaseSpaceTask(Task):
    PROCESS_ENTRY_TASK = None
    LOGGER_NAME = None

    def get_processed_keys(self):
        return []

    def run(self, *args, **kwargs):
        self._logger.info(f"Starting processing prefix {kwargs['prefix']}")
        s3objects_collection = self._bucket.objects.filter(Prefix=kwargs["prefix"])
        self.s3result = list(s3objects_collection)
        self.s3objects = [
            (x.key, x.size)
            for x in s3objects_collection
            if self._regexp.search(x.key.removeprefix(kwargs["prefix"]).lower())
        ]
        processed_keys = self.get_processed_keys()
        for s3object in self.s3objects:
            if s3object[0] not in processed_keys and self.PROCESS_ENTRY_TASK:
                self._logger.debug(f"Creating entry level task with key {s3object[0]}")
                self.PROCESS_ENTRY_TASK.apply_async(
                    (),
                    {"key": s3object[0], "size": s3object[1], "parent_entry_id": kwargs.get("parent_entry_id")},
                    priority=9,
                )
        self._logger.info(f"Ended processing prefix {kwargs['prefix']}")

    def __init__(self):
        session = boto3.session.Session()
        s3 = session.resource(
            "s3",
            region_name=settings.DO_SPACE_DATA_REGION,
            endpoint_url=settings.DO_SPACE_DATA_ENDPOINT_URL,
            aws_access_key_id=settings.DO_SPACE_DATA_KEY,
            aws_secret_access_key=settings.DO_SPACE_DATA_SECRET,
        )
        self._bucket = s3.Bucket(settings.DO_SPACE_DATA_BUCKET)
        self._regexp = re.compile(r"^.[^\/]+(\/|.cb.)$")
        self._logger = get_task_logger(self.LOGGER_NAME)
        self.s3result = None
        self.s3objects = None


class BaseProcessEntryTask(Task):
    NEXT_LEVEL_TASK = None
    MODEL_NAME = None
    APP_LABEL = None
    LOGGER_NAME = None
    PARENT_ENTRY_MODEL_NAME = None
    PARENT_ENTRY_APP_LABEL = None
    PARENT_ENTRY_FIELD = None
    MISSING_ISSUES_TASK = None
    autoretry_for = (DatabaseError,)
    retry_kwargs = {"max_retries": 10}
    retry_backoff = True
    retry_backoff_max = 60

    def check_key_format(self, key):
        return self._key_regexp.match(key.lower())

    def get_defaults(self, **kwargs):
        defaults = {}
        if self.PARENT_ENTRY_MODEL_NAME and "parent_entry_id" in kwargs:
            parent_model = apps.get_model(self.PARENT_ENTRY_APP_LABEL, self.PARENT_ENTRY_MODEL_NAME)
            parent = parent_model.objects.get(pk=kwargs["parent_entry_id"])
            defaults[self.PARENT_ENTRY_FIELD] = parent
        return defaults

    def get_comicvine_id(self, key):
        match = self._id_regexp.match(key.lower())
        return int(match.group("id"))

    def run(self, *args, **kwargs):
        self._logger.info(f"Starting processing key {kwargs['key']}")
        if not self.check_key_format(kwargs["key"]):
            raise WrongKeyFormatError(kwargs["key"])
        comicvine_id = self.get_comicvine_id(kwargs["key"])
        model = apps.get_model(self.APP_LABEL, self.MODEL_NAME)
        self._logger.info(f"Getting/creating entry by comicvine_id {comicvine_id}")
        instance, created, matched = model.objects.get_or_create_from_comicvine(
            comicvine_id, self.get_defaults(**kwargs), force_refresh=True
        )
        if self.MISSING_ISSUES_TASK:
            task = signature(self.MISSING_ISSUES_TASK, kwargs={"pk": instance.pk})
            task.delay()

        if self.NEXT_LEVEL_TASK is not None:
            self._logger.info(f"Creating next level task with prefix {kwargs['key']}")
            # self.NEXT_LEVEL_TASK.delay(prefix=kwargs["key"], parent_entry_id=instance.pk)
            self.NEXT_LEVEL_TASK.apply_async((), {"prefix": kwargs["key"], "parent_entry_id": instance.pk}, priority=9)
        self._logger.info(f"Ended processing key {kwargs['key']}")

    def __init__(self):
        self._id_regexp = re.compile(r"^.*\[(?P<id>\d+)\](\/|.cb.)$")
        self._logger = get_task_logger(self.LOGGER_NAME)


class BaseComicvineInfoTask(Task):
    MODEL_NAME = None
    APP_LABEL = None
    autoretry_for = (OperationalError, DatabaseError)
    retry_kwargs = {"max_retries": None}
    retry_backoff = True
    retry_backoff_max = 60
    MISSING_ISSUES_TASK = None

    def run(self, *args, **kwargs):
        model = apps.get_model(self.APP_LABEL, self.MODEL_NAME)
        pk = kwargs.pop("pk")
        obj = model.objects.get(pk=pk)
        if kwargs.get("force_api_refresh") or not obj.comicvine_actual:
            obj.fill_from_comicvine(**kwargs)
            obj.save()
            if self.MISSING_ISSUES_TASK and (obj.issues.count() > 0 or obj.watchers.count() > 0):
                task = signature(self.MISSING_ISSUES_TASK, kwargs={"pk": obj.pk})
                task.delay()

    def _set_not_matched(self, kwargs):
        model = apps.get_model(self.APP_LABEL, self.MODEL_NAME)
        pk = kwargs["pk"]
        obj = model.objects.get(pk=pk)
        if obj.comicvine_status != model.ComicvineStatus.MATCHED:
            obj.comicvine_status = model.ComicvineStatus.NOT_MATCHED
            obj.save()

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        self._set_not_matched(kwargs)

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        self._set_not_matched(kwargs)


class BaseRefreshTask(Task):
    MODEL_NAME = None
    APP_LABEL = None

    def run(self, *args, **kwargs):
        # Get data from DB
        model = apps.get_model(self.APP_LABEL, self.MODEL_NAME)
        objects_list = list(
            model.objects.exclude(comicvine_status=model.ComicvineStatus.QUEUED).values(
                "id", "comicvine_id", "comicvine_last_match"
            )
        )
        comicvine_ids = [x["comicvine_id"] for x in objects_list]
        objects_map = {
            x["comicvine_id"]: {"id": x["id"], "comicvine_last_match": x["comicvine_last_match"]} for x in objects_list
        }

        # Get data from Mongo
        client = MongoClient(settings.MONGO_URL)
        db = client.get_default_database()
        collection = db[model.MONGO_COLLECTION]
        comicvine_objects = list(collection.find({"id": {"$in": comicvine_ids}}, {"id": 1, "crawl_date": 1}))
        client.close()

        # Starting get data tasks
        for comicvine_object in comicvine_objects:
            obj = objects_map.get(comicvine_object["id"])
            if obj and (
                obj["comicvine_last_match"] is None
                or obj["comicvine_last_match"] <= pytz.UTC.localize(comicvine_object["crawl_date"])
            ):
                model_object = model.objects.get(pk=obj["id"])
                model_object.fill_from_comicvine(delay=True)
                model_object.save()


@shared_task
def full_increment_update() -> None:
    spider_settings = Settings(values=dict(list(spiders_settings_file.__dict__.items())[11:]))
    p = Processor(settings=spider_settings)
    j = Job(FullSpider, incremental="Y")
    p.run(j)


@shared_task
def full_skip_existing_increment_update() -> None:
    spider_settings = Settings(values=dict(list(spiders_settings_file.__dict__.items())[11:]))
    p = Processor(settings=spider_settings)
    j = Job(FullSpider, incremental="Y", skip_existing="Y")
    p.run(j)


@shared_task
def full_skip_existing_update() -> None:
    spider_settings = Settings(values=dict(list(spiders_settings_file.__dict__.items())[11:]))
    p = Processor(settings=spider_settings)
    j = Job(FullSpider, incremental="N", skip_existing="Y")
    p.run(j)


@shared_task
def full_update() -> None:
    spider_settings = Settings(values=dict(list(spiders_settings_file.__dict__.items())[11:]))
    p = Processor(settings=spider_settings)
    j = Job(FullSpider, incremental="N", skip_existing="N")
    p.run(j)
