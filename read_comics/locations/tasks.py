from celery import shared_task
from scrapy.settings import Settings
from spiders.spiders.locations_spider import LocationsSpider
from utils.tasks import BaseComicvineInfoTask, BaseRefreshTask

import read_comics.spiders.settings as spiders_settings_file
from config import celery_app
from read_comics.spiders.scrappyscript import Job, Processor


class LocationComicvineInfoTask(BaseComicvineInfoTask):
    MODEL_NAME = "Location"
    APP_LABEL = "locations"
    MISSING_ISSUES_TASK = "read_comics.missing_issues.tasks.LocationMissingIssuesTask"


location_comicvine_info_task = celery_app.register_task(LocationComicvineInfoTask())


class LocationsRefreshTask(BaseRefreshTask):
    MODEL_NAME = "Location"
    APP_LABEL = "locations"


locations_refresh_task = celery_app.register_task(LocationsRefreshTask())


@shared_task
def locations_increment_update() -> None:
    spider_settings = Settings(values=dict(list(spiders_settings_file.__dict__.items())[11:]))
    p = Processor(settings=spider_settings)
    j = Job(LocationsSpider, incremental="Y", skip_existing="N")
    p.run(j)


@shared_task
def locations_skip_existing_increment_update() -> None:
    spider_settings = Settings(values=dict(list(spiders_settings_file.__dict__.items())[11:]))
    p = Processor(settings=spider_settings)
    j = Job(LocationsSpider, incremental="Y", skip_existing="Y")
    p.run(j)


@shared_task
def locations_skip_existing_update() -> None:
    spider_settings = Settings(values=dict(list(spiders_settings_file.__dict__.items())[11:]))
    p = Processor(settings=spider_settings)
    j = Job(LocationsSpider, incremental="N", skip_existing="Y")
    p.run(j)


@shared_task
def locations_update() -> None:
    spider_settings = Settings(values=dict(list(spiders_settings_file.__dict__.items())[11:]))
    p = Processor(settings=spider_settings)
    j = Job(LocationsSpider, incremental="N", skip_existing="N")
    p.run(j)
