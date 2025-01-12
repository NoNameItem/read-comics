from celery import shared_task
from scrapy.settings import Settings
from scrapyscript import Job, Processor
from spiders.spiders.teams_spider import TeamsSpider
from utils.tasks import BaseComicvineInfoTask, BaseRefreshTask

import read_comics.spiders.settings as spiders_settings_file
from config import celery_app


class TeamComicvineInfoTask(BaseComicvineInfoTask):
    MODEL_NAME = "Team"
    APP_LABEL = "teams"
    MISSING_ISSUES_TASK = "read_comics.missing_issues.tasks.TeamMissingIssuesTask"


team_comicvine_info_task = celery_app.register_task(TeamComicvineInfoTask())


class TeamsRefreshTask(BaseRefreshTask):
    MODEL_NAME = "Team"
    APP_LABEL = "teams"


teams_refresh_task = celery_app.register_task(TeamsRefreshTask())


@shared_task
def teams_increment_update() -> None:
    spider_settings = Settings(values=dict(list(spiders_settings_file.__dict__.items())[11:]))
    p = Processor(settings=spider_settings)
    j = Job(TeamsSpider, incremental="Y", skip_existing="N")
    p.run(j)


@shared_task
def teams_skip_existing_increment_update() -> None:
    spider_settings = Settings(values=dict(list(spiders_settings_file.__dict__.items())[11:]))
    p = Processor(settings=spider_settings)
    j = Job(TeamsSpider, incremental="Y", skip_existing="Y")
    p.run(j)


@shared_task
def teams_skip_existing_update() -> None:
    spider_settings = Settings(values=dict(list(spiders_settings_file.__dict__.items())[11:]))
    p = Processor(settings=spider_settings)
    j = Job(TeamsSpider, incremental="N", skip_existing="Y")
    p.run(j)


@shared_task
def teams_update() -> None:
    spider_settings = Settings(values=dict(list(spiders_settings_file.__dict__.items())[11:]))
    p = Processor(settings=spider_settings)
    j = Job(TeamsSpider, incremental="N", skip_existing="N")
    p.run(j)
