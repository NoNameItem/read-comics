import re

from issues.tasks import issues_space_task
from utils.tasks import (
    BaseComicvineInfoTask,
    BaseProcessEntryTask,
    BaseRefreshTask,
    BaseSpaceTask,
)

from config import celery_app


class VolumeProcessEntryTask(BaseProcessEntryTask):
    MODEL_NAME = 'Volume'
    APP_LABEL = 'volumes'
    LOGGER_NAME = 'VolumeProcessEntryTask'
    PARENT_ENTRY_MODEL_NAME = 'Publisher'
    PARENT_ENTRY_APP_LABEL = 'publishers'
    PARENT_ENTRY_FIELD = 'publisher'
    NEXT_LEVEL_TASK = issues_space_task
    MISSING_ISSUES_TASK = 'read_comics.missing_issues.tasks.VolumeMissingIssuesTask'

    def __init__(self):
        super().__init__()
        self._key_regexp = re.compile(r"^.* \[\d\d\d\d\]\[\d+\]\/$")


volume_entry_task = celery_app.register_task(VolumeProcessEntryTask())


class VolumesSpaceTask(BaseSpaceTask):
    PROCESS_ENTRY_TASK = volume_entry_task
    LOGGER_NAME = "VolumesSpaceTask"


volumes_space_task = celery_app.register_task(VolumesSpaceTask())


class VolumeComicvineInfoTask(BaseComicvineInfoTask):
    MODEL_NAME = 'Volume'
    APP_LABEL = 'volumes'
    MISSING_ISSUES_TASK = 'read_comics.missing_issues.tasks.VolumeMissingIssuesTask'


volume_comicvine_info_task = celery_app.register_task(VolumeComicvineInfoTask())


class VolumesRefreshTask(BaseRefreshTask):
    MODEL_NAME = 'Volume'
    APP_LABEL = 'volumes'


volumes_refresh_task = celery_app.register_task(VolumesRefreshTask())
