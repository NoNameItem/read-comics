from utils.tasks import BaseComicvineInfoTask, BaseRefreshTask

from config import celery_app


class ObjectComicvineInfoTask(BaseComicvineInfoTask):
    MODEL_NAME = "Object"
    APP_LABEL = "objects"
    MISSING_ISSUES_TASK = "read_comics.missing_issues.tasks.ObjectMissingIssuesTask"


object_comicvine_info_task = celery_app.register_task(ObjectComicvineInfoTask())


class ObjectsRefreshTask(BaseRefreshTask):
    MODEL_NAME = "Object"
    APP_LABEL = "objects"


objects_refresh_task = celery_app.register_task(ObjectsRefreshTask())
