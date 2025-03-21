from celery import shared_task
from scrapy.settings import Settings
from spiders.spiders.powers_spider import PowersSpider
from utils.tasks import BaseComicvineInfoTask, BaseRefreshTask

import read_comics.spiders.settings as spiders_settings_file
from config import celery_app
from read_comics.spiders.scrappyscript import Job, Processor


class PowerComicvineInfoTask(BaseComicvineInfoTask):
    MODEL_NAME = "Power"
    APP_LABEL = "powers"


power_comicvine_info_task = celery_app.register_task(PowerComicvineInfoTask())


class PowersRefreshTask(BaseRefreshTask):
    MODEL_NAME = "Power"
    APP_LABEL = "powers"


powers_refresh_task = celery_app.register_task(PowersRefreshTask())


@shared_task
def powers_increment_update() -> None:
    spider_settings = Settings(values=dict(list(spiders_settings_file.__dict__.items())[11:]))
    p = Processor(settings=spider_settings)
    j = Job(PowersSpider, incremental="Y", skip_existing="N")
    p.run(j)


@shared_task
def powers_skip_existing_increment_update() -> None:
    spider_settings = Settings(values=dict(list(spiders_settings_file.__dict__.items())[11:]))
    p = Processor(settings=spider_settings)
    j = Job(PowersSpider, incremental="Y", skip_existing="Y")
    p.run(j)


@shared_task
def powers_skip_existing_update() -> None:
    spider_settings = Settings(values=dict(list(spiders_settings_file.__dict__.items())[11:]))
    p = Processor(settings=spider_settings)
    j = Job(PowersSpider, incremental="N", skip_existing="Y")
    p.run(j)


@shared_task
def powers_update() -> None:
    spider_settings = Settings(values=dict(list(spiders_settings_file.__dict__.items())[11:]))
    p = Processor(settings=spider_settings)
    j = Job(PowersSpider, incremental="N", skip_existing="N")
    p.run(j)
