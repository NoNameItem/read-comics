from django.db.models import Q
from django.utils import timezone

from read_comics.missing_issues.models import MissingIssue


def get_watched_missing_issues_query(user, search_query=None):
    today = timezone.localdate()

    def get_subquery(field):
        f = {f"{field}__watchers__user": user}

        q = MissingIssue.objects.visible(today).filter(**f)

        if search_query:
            return q.filter(
                Q(publisher_name__icontains=search_query)
                | Q(volume_name__icontains=search_query)
                | Q(name__icontains=search_query)
            )

        return q

    return (
        get_subquery("characters")
        .union(get_subquery("concepts"))
        .union(get_subquery("locations"))
        .union(get_subquery("objects_in"))
        .union(get_subquery("people"))
        .union(get_subquery("story_arcs"))
        .union(get_subquery("teams"))
        .union(get_subquery("volume"))
        .union(get_subquery("publisher"))
    )
