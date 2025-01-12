from celery import shared_task
from scrapy.settings import Settings
from scrapyscript import Job, Processor
from spiders.spiders.story_arcs_spider import StoryArcsSpider
from utils.tasks import BaseComicvineInfoTask, BaseRefreshTask

import read_comics.spiders.settings as spiders_settings_file
from config import celery_app


class StoryArcComicvineInfoTask(BaseComicvineInfoTask):
    MODEL_NAME = "StoryArc"
    APP_LABEL = "story_arcs"
    MISSING_ISSUES_TASK = "read_comics.missing_issues.tasks.StoryArcMissingIssuesTask"


story_arc_comicvine_info_task = celery_app.register_task(StoryArcComicvineInfoTask())


class StoryArcsRefreshTask(BaseRefreshTask):
    MODEL_NAME = "StoryArc"
    APP_LABEL = "story_arcs"


story_arcs_refresh_task = celery_app.register_task(StoryArcsRefreshTask())


@shared_task
def story_arcs_increment_update() -> None:
    spider_settings = Settings(values=dict(list(spiders_settings_file.__dict__.items())[11:]))
    p = Processor(settings=spider_settings)
    j = Job(StoryArcsSpider, incremental="Y", skip_existing="N")
    p.run(j)


@shared_task
def story_arcs_skip_existing_increment_update() -> None:
    spider_settings = Settings(values=dict(list(spiders_settings_file.__dict__.items())[11:]))
    p = Processor(settings=spider_settings)
    j = Job(StoryArcsSpider, incremental="Y", skip_existing="Y")
    p.run(j)


@shared_task
def story_arcs_skip_existing_update() -> None:
    spider_settings = Settings(values=dict(list(spiders_settings_file.__dict__.items())[11:]))
    p = Processor(settings=spider_settings)
    j = Job(StoryArcsSpider, incremental="N", skip_existing="Y")
    p.run(j)


@shared_task
def story_arcs_update() -> None:
    spider_settings = Settings(values=dict(list(spiders_settings_file.__dict__.items())[11:]))
    p = Processor(settings=spider_settings)
    j = Job(StoryArcsSpider, incremental="N", skip_existing="N")
    p.run(j)
