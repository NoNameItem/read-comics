from django.db.models import Count, F, Func, Q, TextField, Value
from django.db.models.functions import Concat

from read_comics.characters.models import Character
from read_comics.issues.models import Issue
from read_comics.story_arcs.models import StoryArc
from read_comics.teams.models import Team
from read_comics.volumes.models import Volume


def get_issues_queryset(publisher):
    return Issue.objects.filter(comicvine_status='MATCHED').filter(volume__publisher=publisher).order_by(
        'cover_date', 'volume__name', 'volume__start_year', 'numerical_number', 'number'
    ).annotate(
        parent_slug=Value(publisher.slug),
        badge_name=Concat(
            F('volume__name'), Value(' ('), F('volume__start_year'), Value(') #'), F('number'), Value(' '), F('name'),
            output_field=TextField()
        ),
        group_breaker=Func(F('cover_date'), Value('Month YYYY'), function='to_char', output_field=TextField()),
        desc=F('cover_date')
    )


def get_volumes_queryset(publisher):
    return Volume.objects.filter(
        publisher=publisher
    ).filter(comicvine_status='MATCHED').annotate(
        issues_count=Count('issues'),
        badge_name=Concat(F('name'), Value(' ('), F('start_year'), Value(')'),
                          output_field=TextField()),
        desc=Concat(F('issues_count'), Value(' issue(s)'), output_field=TextField())
    ).order_by('name', 'start_year')


def get_characters_queryset(publisher):
    return Character.objects.filter(publisher=publisher).annotate(
        issues_count=Count('issues', filter=Q(issues__volume__publisher=publisher)),
        desc=Concat(Value('Appeared in '), F('issues_count'), Value(' issue(s)'), output_field=TextField())
    ).order_by('-issues_count', 'name', 'id')


def get_story_arcs_queryset(publisher):
    return StoryArc.objects.filter(publisher=publisher).distinct().order_by('name', 'id')


def get_teams_queryset(publisher):
    return Team.objects.filter(publisher=publisher).annotate(
        issues_count=Count('issues', filter=Q(issues__volume__publisher=publisher)),
        desc=Concat(Value('Appeared in '), F('issues_count'), Value(' issue(s)'), output_field=TextField())
    ).order_by('-issues_count', 'name', 'id')
