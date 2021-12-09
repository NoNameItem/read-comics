from utils.tasks import BaseComicvineInfoTask, BaseRefreshTask

from config import celery_app


class CharacterComicvineInfoTask(BaseComicvineInfoTask):
    MODEL_NAME = 'Character'
    APP_LABEL = 'characters'
    MISSING_ISSUES_TASK = 'read_comics.missing_issues.tasks.CharacterMissingIssuesTask'


character_comicvine_info_task = celery_app.register_task(CharacterComicvineInfoTask())


class CharactersRefreshTask(BaseRefreshTask):
    MODEL_NAME = 'Character'
    APP_LABEL = 'characters'


characters_refresh_task = celery_app.register_task(CharactersRefreshTask())
