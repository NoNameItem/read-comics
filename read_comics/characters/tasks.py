from celery import shared_task
from scrapy.settings import Settings
from scrapyscript import Job, Processor
from utils.tasks import BaseComicvineInfoTask, BaseRefreshTask

import read_comics.spiders.settings as spiders_settings_file
from config import celery_app
from read_comics.spiders.spiders.characters_spider import CharactersSpider


class CharacterComicvineInfoTask(BaseComicvineInfoTask):
    MODEL_NAME = "Character"
    APP_LABEL = "characters"
    MISSING_ISSUES_TASK = "read_comics.missing_issues.tasks.CharacterMissingIssuesTask"


character_comicvine_info_task = celery_app.register_task(CharacterComicvineInfoTask())


class CharactersRefreshTask(BaseRefreshTask):
    MODEL_NAME = "Character"
    APP_LABEL = "characters"


characters_refresh_task = celery_app.register_task(CharactersRefreshTask())


@shared_task
def characters_increment_update() -> None:
    spider_settings = Settings(values=dict(list(spiders_settings_file.__dict__.items())[11:]))
    p = Processor(settings=spider_settings)
    j = Job(CharactersSpider, incremental="Y")
    p.run(j)
