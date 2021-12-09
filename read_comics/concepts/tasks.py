from utils.tasks import BaseComicvineInfoTask, BaseRefreshTask

from config import celery_app


class ConceptComicvineInfoTask(BaseComicvineInfoTask):
    MODEL_NAME = 'Concept'
    APP_LABEL = 'concepts'
    MISSING_ISSUES_TASK = 'read_comics.missing_issues.tasks.ConceptMissingIssuesTask'


concept_comicvine_info_task = celery_app.register_task(ConceptComicvineInfoTask())


class ConceptsRefreshTask(BaseRefreshTask):
    MODEL_NAME = 'Concept'
    APP_LABEL = 'concepts'


concepts_refresh_task = celery_app.register_task(ConceptsRefreshTask())
