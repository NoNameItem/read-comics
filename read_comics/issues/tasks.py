import re

import boto3
from celery import shared_task
from django.apps import apps
from django.conf import settings
from scrapy.settings import Settings
from scrapyscript import Job, Processor
from spiders.spiders.issues_spider import IssuesSpider
from utils.tasks import BaseComicvineInfoTask, BaseProcessEntryTask, BaseRefreshTask, BaseSpaceTask

import read_comics.spiders.settings as spiders_settings_file
from config import celery_app


class IssueProcessEntryTask(BaseProcessEntryTask):
    MODEL_NAME = "Issue"
    APP_LABEL = "issues"
    LOGGER_NAME = "IssueProcessEntryTask"
    PARENT_ENTRY_MODEL_NAME = "Volume"
    PARENT_ENTRY_APP_LABEL = "volumes"
    PARENT_ENTRY_FIELD = "volume"

    def get_defaults(self, **kwargs):
        defaults = super(IssueProcessEntryTask, self).get_defaults(**kwargs)
        defaults["space_key"] = kwargs["key"]
        defaults["size"] = kwargs["size"]
        return defaults

    def __init__(self):
        super().__init__()
        self._key_regexp = re.compile(r"^.* #[^ \[\]]+ \[\d+\]\.cb.$")


issue_entry_task = celery_app.register_task(IssueProcessEntryTask())


class IssuesSpaceTask(BaseSpaceTask):
    PROCESS_ENTRY_TASK = issue_entry_task
    LOGGER_NAME = "IssuesSpaceTask"

    def get_processed_keys(self):
        model = apps.get_model("issues", "Issue")
        return set(model.objects.matched().values_list("space_key", flat=True))


issues_space_task = celery_app.register_task(IssuesSpaceTask())


class IssueComicvineInfoTask(BaseComicvineInfoTask):
    MODEL_NAME = "Issue"
    APP_LABEL = "issues"


issue_comicvine_info_task = celery_app.register_task(IssueComicvineInfoTask())


class IssuesRefreshTask(BaseRefreshTask):
    MODEL_NAME = "Issue"
    APP_LABEL = "issues"


issues_refresh_task = celery_app.register_task(IssuesRefreshTask())


@shared_task
def purge_deleted():
    model = apps.get_model("issues", "Issue")
    session = boto3.session.Session()
    s3 = session.resource("s3", region_name=settings.DO_SPACE_DATA_REGION,
                          endpoint_url=settings.DO_SPACE_DATA_ENDPOINT_URL,
                          aws_access_key_id=settings.DO_SPACE_DATA_KEY,
                          aws_secret_access_key=settings.DO_SPACE_DATA_SECRET)
    bucket = s3.Bucket(settings.DO_SPACE_DATA_BUCKET)
    objs = [x.key for x in bucket.objects.all()]
    model.objects.exclude(space_key__in=objs).delete()


@shared_task
def issues_increment_update() -> None:
    spider_settings = Settings(values=dict(list(spiders_settings_file.__dict__.items())[11:]))
    p = Processor(settings=spider_settings)
    j = Job(IssuesSpider, incremental="Y")
    p.run(j)
