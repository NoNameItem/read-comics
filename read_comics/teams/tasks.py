from utils.tasks import BaseComicvineInfoTask, BaseRefreshTask

from config import celery_app


class TeamComicvineInfoTask(BaseComicvineInfoTask):
    MODEL_NAME = "Team"
    APP_LABEL = "teams"
    MISSING_ISSUES_TASK = "read_comics.missing_issues.tasks.TeamMissingIssuesTask"


team_comicvine_info_task = celery_app.register_task(TeamComicvineInfoTask())


class TeamsRefreshTask(BaseRefreshTask):
    MODEL_NAME = "Team"
    APP_LABEL = "teams"


teams_refresh_task = celery_app.register_task(TeamsRefreshTask())
