from celery import shared_task
from scrapy.settings import Settings
from spiders.spiders.people_spider import PeopleSpider
from utils.tasks import BaseComicvineInfoTask, BaseRefreshTask

import read_comics.spiders.settings as spiders_settings_file
from config import celery_app
from read_comics.spiders.scrappyscript import Job, Processor


class PersonComicvineInfoTask(BaseComicvineInfoTask):
    MODEL_NAME = "Person"
    APP_LABEL = "people"
    MISSING_ISSUES_TASK = "read_comics.missing_issues.tasks.PersonMissingIssuesTask"


person_comicvine_info_task = celery_app.register_task(PersonComicvineInfoTask())


class PeopleRefreshTask(BaseRefreshTask):
    MODEL_NAME = "Person"
    APP_LABEL = "people"


people_refresh_task = celery_app.register_task(PeopleRefreshTask())


@shared_task
def people_increment_update() -> None:
    spider_settings = Settings(values=dict(list(spiders_settings_file.__dict__.items())[11:]))
    p = Processor(settings=spider_settings)
    j = Job(PeopleSpider, incremental="Y", skip_existing="N")
    p.run(j)


@shared_task
def people_skip_existing_increment_update() -> None:
    spider_settings = Settings(values=dict(list(spiders_settings_file.__dict__.items())[11:]))
    p = Processor(settings=spider_settings)
    j = Job(PeopleSpider, incremental="Y", skip_existing="Y")
    p.run(j)


@shared_task
def people_skip_existing_update() -> None:
    spider_settings = Settings(values=dict(list(spiders_settings_file.__dict__.items())[11:]))
    p = Processor(settings=spider_settings)
    j = Job(PeopleSpider, incremental="N", skip_existing="Y")
    p.run(j)


@shared_task
def people_update() -> None:
    spider_settings = Settings(values=dict(list(spiders_settings_file.__dict__.items())[11:]))
    p = Processor(settings=spider_settings)
    j = Job(PeopleSpider, incremental="N", skip_existing="N")
    p.run(j)
