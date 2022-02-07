from utils.tasks import BaseComicvineInfoTask, BaseRefreshTask

from config import celery_app


class PowerComicvineInfoTask(BaseComicvineInfoTask):
    MODEL_NAME = "Power"
    APP_LABEL = "powers"


power_comicvine_info_task = celery_app.register_task(PowerComicvineInfoTask())


class PowersRefreshTask(BaseRefreshTask):
    MODEL_NAME = "Power"
    APP_LABEL = "powers"


powers_refresh_task = celery_app.register_task(PowersRefreshTask())
