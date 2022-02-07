from utils.tasks import BaseComicvineInfoTask, BaseRefreshTask

from config import celery_app


class LocationComicvineInfoTask(BaseComicvineInfoTask):
    MODEL_NAME = "Location"
    APP_LABEL = "locations"
    MISSING_ISSUES_TASK = "read_comics.missing_issues.tasks.LocationMissingIssuesTask"


location_comicvine_info_task = celery_app.register_task(LocationComicvineInfoTask())


class LocationsRefreshTask(BaseRefreshTask):
    MODEL_NAME = "Location"
    APP_LABEL = "locations"


locations_refresh_task = celery_app.register_task(LocationsRefreshTask())
