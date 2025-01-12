from celery import shared_task
from scrapy.settings import Settings
from scrapyscript import Job, Processor
from spiders.spiders.objects_spider import ObjectsSpider
from utils.tasks import BaseComicvineInfoTask, BaseRefreshTask

import read_comics.spiders.settings as spiders_settings_file
from config import celery_app


class ObjectComicvineInfoTask(BaseComicvineInfoTask):
    MODEL_NAME = "Object"
    APP_LABEL = "objects"
    MISSING_ISSUES_TASK = "read_comics.missing_issues.tasks.ObjectMissingIssuesTask"


object_comicvine_info_task = celery_app.register_task(ObjectComicvineInfoTask())


class ObjectsRefreshTask(BaseRefreshTask):
    MODEL_NAME = "Object"
    APP_LABEL = "objects"


objects_refresh_task = celery_app.register_task(ObjectsRefreshTask())


@shared_task
def objects_increment_update() -> None:
    spider_settings = Settings(values=dict(list(spiders_settings_file.__dict__.items())[11:]))
    p = Processor(settings=spider_settings)
    j = Job(ObjectsSpider, incremental="Y", skip_existing="N")
    p.run(j)


@shared_task
def objects_skip_existing_increment_update() -> None:
    spider_settings = Settings(values=dict(list(spiders_settings_file.__dict__.items())[11:]))
    p = Processor(settings=spider_settings)
    j = Job(ObjectsSpider, incremental="Y", skip_existing="Y")
    p.run(j)


@shared_task
def objects_skip_existing_update() -> None:
    spider_settings = Settings(values=dict(list(spiders_settings_file.__dict__.items())[11:]))
    p = Processor(settings=spider_settings)
    j = Job(ObjectsSpider, incremental="N", skip_existing="Y")
    p.run(j)


@shared_task
def objects_update() -> None:
    spider_settings = Settings(values=dict(list(spiders_settings_file.__dict__.items())[11:]))
    p = Processor(settings=spider_settings)
    j = Job(ObjectsSpider, incremental="N", skip_existing="N")
    p.run(j)
