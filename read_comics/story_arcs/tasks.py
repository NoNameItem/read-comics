from utils.tasks import BaseComicvineInfoTask, BaseRefreshTask

from config import celery_app


class StoryArcComicvineInfoTask(BaseComicvineInfoTask):
    MODEL_NAME = 'StoryArc'
    APP_LABEL = 'story_arcs'


story_arc_comicvine_info_task = celery_app.register_task(StoryArcComicvineInfoTask())


class StoryArcsRefreshTask(BaseRefreshTask):
    MODEL_NAME = 'StoryArc'
    APP_LABEL = 'story_arcs'


story_arcs_refresh_task = celery_app.register_task(StoryArcsRefreshTask())
