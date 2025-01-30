from celery import shared_task
from scrapy.settings import Settings
from spiders.spiders.concepts_spider import ConceptsSpider
from utils.tasks import BaseComicvineInfoTask, BaseRefreshTask

import read_comics.spiders.settings as spiders_settings_file
from config import celery_app
from read_comics.spiders.scrappyscript import Job, Processor


class ConceptComicvineInfoTask(BaseComicvineInfoTask):
    MODEL_NAME = "Concept"
    APP_LABEL = "concepts"
    MISSING_ISSUES_TASK = "read_comics.missing_issues.tasks.ConceptMissingIssuesTask"


concept_comicvine_info_task = celery_app.register_task(ConceptComicvineInfoTask())


class ConceptsRefreshTask(BaseRefreshTask):
    MODEL_NAME = "Concept"
    APP_LABEL = "concepts"


concepts_refresh_task = celery_app.register_task(ConceptsRefreshTask())


@shared_task
def concepts_increment_update() -> None:
    spider_settings = Settings(values=dict(list(spiders_settings_file.__dict__.items())[11:]))
    p = Processor(settings=spider_settings)
    j = Job(ConceptsSpider, incremental="Y", skip_existing="N")
    p.run(j)


@shared_task
def concepts_skip_existing_increment_update() -> None:
    spider_settings = Settings(values=dict(list(spiders_settings_file.__dict__.items())[11:]))
    p = Processor(settings=spider_settings)
    j = Job(ConceptsSpider, incremental="Y", skip_existing="Y")
    p.run(j)


@shared_task
def concepts_skip_existing_update() -> None:
    spider_settings = Settings(values=dict(list(spiders_settings_file.__dict__.items())[11:]))
    p = Processor(settings=spider_settings)
    j = Job(ConceptsSpider, incremental="N", skip_existing="Y")
    p.run(j)


@shared_task
def concepts_update() -> None:
    spider_settings = Settings(values=dict(list(spiders_settings_file.__dict__.items())[11:]))
    p = Processor(settings=spider_settings)
    j = Job(ConceptsSpider, incremental="N", skip_existing="N")
    p.run(j)
