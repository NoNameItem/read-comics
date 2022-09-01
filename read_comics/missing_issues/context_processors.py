from read_comics.missing_issues.models import MissingIssue
from read_comics.missing_issues.queries import get_watched_missing_issues_query


def missing_issues_count(_request):
    if _request.user.is_staff or _request.user.is_superuser:
        return {
            "total_missing_issues_count": MissingIssue.objects.filter(skip=False).count(),
            "watched_missing_issues_count": get_watched_missing_issues_query(_request.user).count(),
        }
    else:
        return {}
