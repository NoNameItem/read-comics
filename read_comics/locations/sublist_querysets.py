from django.db.models import Count, F, TextField, Value
from django.db.models.functions import Concat

from read_comics.volumes.models import Volume


def get_issues_queryset(location):
    return location.issues.order_by('cover_date', 'volume__name', 'volume__start_year', 'numerical_number', 'number') \
        .annotate(
        parent_slug=Value(location.slug),
        badge_name=Concat(
            F('volume__name'), Value(' ('), F('volume__start_year'), Value(') #'), F('number'), Value(' '), F('name'),
            output_field=TextField()
        ),
        desc=F('cover_date')
    )


def get_volumes_queryset(location):
    return Volume.objects.filter(
        issues__in=location.issues.all()
    ).annotate(
        issues_count=Count('issues'),
        badge_name=Concat(F('name'), Value(' ('), F('start_year'), Value(')'),
                          output_field=TextField()),
        desc=Concat(F('issues_count'), Value(' issue(s)'), output_field=TextField())
    ).order_by('-issues_count')
