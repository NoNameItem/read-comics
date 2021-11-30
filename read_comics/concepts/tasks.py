from utils.tasks import BaseComicvineInfoTask, BaseRefreshTask

from config import celery_app


class ConceptComicvineInfoTask(BaseComicvineInfoTask):
    MODEL_NAME = 'Concept'
    APP_LABEL = 'concepts'


concept_comicvine_info_task = celery_app.register_task(ConceptComicvineInfoTask())


class ConceptsRefreshTask(BaseRefreshTask):
    MODEL_NAME = 'Concept'
    APP_LABEL = 'concepts'


concepts_refresh_task = celery_app.register_task(ConceptsRefreshTask())
