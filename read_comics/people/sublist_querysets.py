from django.db.models import Count, F, TextField, Value
from django.db.models.functions import Concat

from read_comics.volumes.models import Volume


def get_issues_queryset(location):
    return location.issues.filter(comicvine_status='MATCHED').order_by('cover_date', 'volume__name',
                                                                       'volume__start_year', 'numerical_number',
                                                                       'number') \
        .annotate(
        parent_slug=Value(location.slug),
        badge_name=Concat(
            F('volume__name'), Value(' ('), F('volume__start_year'), Value(') #'), F('number'), Value(' '), F('name'),
            output_field=TextField()
        ),
        desc=F('cover_date')
    )


def get_volumes_queryset(person):
    return Volume.objects.filter(
        issues__in=person.issues.all()
    ).filter(comicvine_status='MATCHED').annotate(
        issues_count=Count('issues'),
        badge_name=Concat(F('name'), Value(' ('), F('start_year'), Value(')'),
                          output_field=TextField()),
        desc=Concat(F('issues_count'), Value(' issue(s)'), output_field=TextField())
    ).order_by('start_year', 'name')


def get_characters_queryset(person):
    return person.created_characters.all().order_by('name', 'id')
