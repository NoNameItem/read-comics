import re

from celery import shared_task
from django.apps import apps
from issues.tasks import issues_space_task
from scrapy.settings import Settings
from scrapyscript import Job, Processor
from spiders.spiders.volumes_spider import VolumesSpider
from utils.tasks import BaseComicvineInfoTask, BaseProcessEntryTask, BaseRefreshTask, BaseSpaceTask

import read_comics.spiders.settings as spiders_settings_file
from config import celery_app


class VolumeProcessEntryTask(BaseProcessEntryTask):
    MODEL_NAME = "Volume"
    APP_LABEL = "volumes"
    LOGGER_NAME = "VolumeProcessEntryTask"
    PARENT_ENTRY_MODEL_NAME = "Publisher"
    PARENT_ENTRY_APP_LABEL = "publishers"
    PARENT_ENTRY_FIELD = "publisher"
    NEXT_LEVEL_TASK = issues_space_task
    MISSING_ISSUES_TASK = "read_comics.missing_issues.tasks.VolumeMissingIssuesTask"

    def __init__(self):
        super().__init__()
        self._key_regexp = re.compile(r"^.* \[\d\d\d\d\] \[\d+\]\/$")


volume_entry_task = celery_app.register_task(VolumeProcessEntryTask())


class VolumesSpaceTask(BaseSpaceTask):
    PROCESS_ENTRY_TASK = volume_entry_task
    LOGGER_NAME = "read_comics.tasks.VolumesSpaceTask"

    def get_processed_keys(self):
        model = apps.get_model("issues", "Issue")
        issues_keys = set(model.objects.matched().values_list("space_key", flat=True))

        processed_keys = []
        for volume, _ in self.s3objects:
            new_issues = [
                x
                for x in self.s3result
                if x.key.startswith(volume) and x.key not in issues_keys and x.key != volume
            ]
            if not new_issues:
                processed_keys.append(volume)

        return processed_keys


volumes_space_task = celery_app.register_task(VolumesSpaceTask())


class VolumeComicvineInfoTask(BaseComicvineInfoTask):
    MODEL_NAME = "Volume"
    APP_LABEL = "volumes"
    MISSING_ISSUES_TASK = "read_comics.missing_issues.tasks.VolumeMissingIssuesTask"


volume_comicvine_info_task = celery_app.register_task(VolumeComicvineInfoTask())


class VolumesRefreshTask(BaseRefreshTask):
    MODEL_NAME = "Volume"
    APP_LABEL = "volumes"


volumes_refresh_task = celery_app.register_task(VolumesRefreshTask())


@shared_task
def volumes_increment_update() -> None:
    spider_settings = Settings(values=dict(list(spiders_settings_file.__dict__.items())[11:]))
    p = Processor(settings=spider_settings)
    j = Job(VolumesSpider, incremental="Y")
    p.run(j)
