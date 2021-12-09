import re

import boto3
import pytz
from celery import Task, signature
from celery.utils.log import get_task_logger
from django.apps import apps
from django.conf import settings
from django.db import OperationalError
from pymongo import MongoClient


class BaseSpaceTask(Task):
    PROCESS_ENTRY_TASK = None
    LOGGER_NAME = None

    def get_processed_keys(self):
        return []

    def run(self, *args, **kwargs):
        self._logger.debug("Starting processing prefix {0}".format(kwargs['prefix']))
        s3objects_collection = self._bucket.objects.filter(Prefix=kwargs['prefix'])
        s3objects = [
            (x.key, x.size)
            for x in s3objects_collection
            if self._regexp.search(x.key.removeprefix(kwargs['prefix']).lower())
        ]
        for s3object in s3objects:
            processed_keys = self.get_processed_keys()
            if s3object[0] not in processed_keys:
                if self.PROCESS_ENTRY_TASK:
                    self._logger.debug("Creating entry level task with key {0}".format(s3object[0]))
                    self.PROCESS_ENTRY_TASK.apply_async(
                        (),
                        {
                            'key': s3object[0],
                            'size': s3object[1],
                            'parent_entry_id': kwargs.get('parent_entry_id')
                        },
                        priority=0
                    )
        self._logger.debug("Ended processing prefix {0}".format(kwargs['prefix']))

    def __init__(self):
        session = boto3.session.Session()
        s3 = session.resource('s3', region_name=settings.DO_SPACE_DATA_REGION,
                              endpoint_url=settings.DO_SPACE_DATA_ENDPOINT_URL,
                              aws_access_key_id=settings.DO_SPACE_DATA_KEY,
                              aws_secret_access_key=settings.DO_SPACE_DATA_SECRET)
        self._bucket = s3.Bucket(settings.DO_SPACE_DATA_BUCKET)
        self._regexp = re.compile(r"^.[^\/]+(\/|.cb.)$")
        self._logger = get_task_logger(self.LOGGER_NAME)


class BaseProcessEntryTask(Task):
    NEXT_LEVEL_TASK = None
    MODEL_NAME = None
    APP_LABEL = None
    LOGGER_NAME = None
    PARENT_ENTRY_MODEL_NAME = None
    PARENT_ENTRY_APP_LABEL = None
    PARENT_ENTRY_FIELD = None
    MISSING_ISSUES_TASK = None

    def get_defaults(self, **kwargs):
        defaults = dict()
        if self.PARENT_ENTRY_MODEL_NAME:
            parent_model = apps.get_model(self.PARENT_ENTRY_APP_LABEL, self.PARENT_ENTRY_MODEL_NAME)
            parent = parent_model.objects.get(pk=kwargs['parent_entry_id'])
            defaults[self.PARENT_ENTRY_FIELD] = parent
        return defaults

    def get_comicvine_id(self, key):
        match = self._id_regexp.match(key.lower())
        comicvine_id = int(match.group('id'))
        return comicvine_id

    def run(self, *args, **kwargs):
        self._logger.debug("Starting processing key {0}".format(kwargs['key']))
        comicvine_id = self.get_comicvine_id(kwargs['key'])
        model = apps.get_model(self.APP_LABEL, self.MODEL_NAME)
        instance, created, matched = model.objects.get_or_create_from_comicvine(
            comicvine_id,
            self.get_defaults(**kwargs),
            force_refresh=True
        )
        if self.MISSING_ISSUES_TASK:
            task = signature(self.MISSING_ISSUES_TASK, kwargs={'pk': instance.pk})
            task.delay()

        if self.NEXT_LEVEL_TASK is not None:
            self._logger.debug("Creating next level task with prefix {0}".format(kwargs['key']))
            # self.NEXT_LEVEL_TASK.delay(prefix=kwargs['key'], parent_entry_id=instance.pk)
            self.NEXT_LEVEL_TASK.apply_async(
                (),
                {
                    'prefix': kwargs['key'],
                    'parent_entry_id': instance.pk
                },
                priority=0
            )
        self._logger.debug("Ended processing key {0}".format(kwargs['key']))

    def __init__(self):
        self._id_regexp = re.compile(r"^.*\[(?P<id>\d+)\](\/|.cb.)$")
        self._logger = get_task_logger(self.LOGGER_NAME)


class BaseComicvineInfoTask(Task):
    MODEL_NAME = None
    APP_LABEL = None
    autoretry_for = (OperationalError,)
    retry_kwargs = {'max_retries': None}
    retry_backoff = True
    retry_backoff_max = 60
    MISSING_ISSUES_TASK = None

    def run(self, *args, **kwargs):
        model = apps.get_model(self.APP_LABEL, self.MODEL_NAME)
        pk = kwargs['pk']
        obj = model.objects.get(pk=pk)
        if not obj.comicvine_actual:
            obj.fill_from_comicvine(kwargs['follow_m2m'])
            obj.save()
            if self.MISSING_ISSUES_TASK:
                task = signature(self.MISSING_ISSUES_TASK, kwargs={'pk': obj.pk})
                task.delay()

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        model = apps.get_model(self.APP_LABEL, self.MODEL_NAME)
        pk = kwargs['pk']
        obj = model.objects.get(pk=pk)
        if obj.comicvine_status != model.ComicvineStatus.MATCHED:
            obj.comicvine_status = model.ComicvineStatus.NOT_MATCHED
            obj.save()


class BaseRefreshTask(Task):
    MODEL_NAME = None
    APP_LABEL = None

    def run(self, *args, **kwargs):
        # Get data from DB
        model = apps.get_model(self.APP_LABEL, self.MODEL_NAME)
        objects_list = list(
            model.objects.exclude(
                comicvine_status=model.ComicvineStatus.QUEUED
            ).values(
                'id',
                'comicvine_id',
                'comicvine_last_match'
            )
        )
        comicvine_ids = [x['comicvine_id'] for x in objects_list]
        objects_map = {
            x['comicvine_id']: {
                'id': x['id'],
                'comicvine_last_match': x['comicvine_last_match']
            }
            for x in objects_list
        }

        # Get data from Mongo
        client = MongoClient(settings.MONGO_URL)
        db = client.get_default_database()
        collection = db[model.MONGO_COLLECTION]
        comicvine_objects = list(collection.find({'id': {'$in': comicvine_ids}}, {'id': 1, 'crawl_date': 1}))

        # Starting get data tasks
        for comicvine_object in comicvine_objects:
            obj = objects_map.get(comicvine_object['id'])
            if obj:
                if obj['comicvine_last_match'] is None \
                   or obj['comicvine_last_match'] <= pytz.UTC.localize(comicvine_object['crawl_date']):
                    model_object = model.objects.get(pk=obj['id'])
                    model_object.fill_from_comicvine(delay=True)
                    model_object.save()
