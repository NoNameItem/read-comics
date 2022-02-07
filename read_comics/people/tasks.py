from utils.tasks import BaseComicvineInfoTask, BaseRefreshTask

from config import celery_app


class PersonComicvineInfoTask(BaseComicvineInfoTask):
    MODEL_NAME = "Person"
    APP_LABEL = "people"
    MISSING_ISSUES_TASK = "read_comics.missing_issues.tasks.PersonMissingIssuesTask"


person_comicvine_info_task = celery_app.register_task(PersonComicvineInfoTask())


class PeopleRefreshTask(BaseRefreshTask):
    MODEL_NAME = "Person"
    APP_LABEL = "people"


people_refresh_task = celery_app.register_task(PeopleRefreshTask())
