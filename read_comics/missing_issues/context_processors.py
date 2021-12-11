from read_comics.missing_issues.models import MissingIssue


def missing_issues_count(_request):
    if _request.user.is_staff or _request.user.is_superuser:
        return {"missing_issues_count": MissingIssue.objects.count()}
    else:
        return {}
