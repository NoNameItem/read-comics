import re

from celery import shared_task
from scrapy.settings import Settings
from scrapyscript import Job, Processor
from spiders.spiders.publishers_spider import PublishersSpider
from utils.tasks import BaseComicvineInfoTask, BaseProcessEntryTask, BaseRefreshTask, BaseSpaceTask
from volumes.tasks import volumes_space_task

import read_comics.spiders.settings as spiders_settings_file
from config import celery_app


class PublisherProcessEntryTask(BaseProcessEntryTask):
    MODEL_NAME = "Publisher"
    APP_LABEL = "publishers"
    LOGGER_NAME = "VolumeProcessEntryTask"
    NEXT_LEVEL_TASK = volumes_space_task

    def __init__(self):
        super().__init__()
        self._key_regexp = re.compile(r"^.*\[\d+\]\/$")


publisher_entry_task = celery_app.register_task(PublisherProcessEntryTask())


class PublishersSpaceTask(BaseSpaceTask):
    PROCESS_ENTRY_TASK = publisher_entry_task
    LOGGER_NAME = "PublishersSpaceTask"


publishers_space_task = celery_app.register_task(PublishersSpaceTask())


class PublisherComicvineInfoTask(BaseComicvineInfoTask):
    MODEL_NAME = "Publisher"
    APP_LABEL = "publishers"


publisher_comicvine_info_task = celery_app.register_task(PublisherComicvineInfoTask())


class PublishersRefreshTask(BaseRefreshTask):
    MODEL_NAME = "Publisher"
    APP_LABEL = "publishers"


publishers_refresh_task = celery_app.register_task(PublishersRefreshTask())


@shared_task
def publishers_increment_update() -> None:
    spider_settings = Settings(values=dict(list(spiders_settings_file.__dict__.items())[11:]))
    p = Processor(settings=spider_settings)
    j = Job(PublishersSpider, incremental="Y")
    p.run(j)
