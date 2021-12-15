from read_comics.missing_issues.models import MissingIssue


def get_watched_missing_issues_query(user):
    return MissingIssue.objects.filter(characters__watchers__user=user, skip=False).union(
        MissingIssue.objects.filter(concepts__watchers__user=user, skip=False)
    ).union(
        MissingIssue.objects.filter(locations__watchers__user=user, skip=False)
    ).union(
        MissingIssue.objects.filter(objects_in__watchers__user=user, skip=False)
    ).union(
        MissingIssue.objects.filter(people__watchers__user=user, skip=False)
    ).union(
        MissingIssue.objects.filter(story_arcs__watchers__user=user, skip=False)
    ).union(
        MissingIssue.objects.filter(teams__watchers__user=user, skip=False)
    ).union(
        MissingIssue.objects.filter(volume__watchers__user=user, skip=False)
    ).union(
        MissingIssue.objects.filter(publisher__watchers__user=user, skip=False)
    )
