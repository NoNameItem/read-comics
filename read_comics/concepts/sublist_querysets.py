from django.db.models import Count, F, Func, Q, TextField, Value
from django.db.models.functions import Concat

from read_comics.volumes.models import Volume


def get_issues_queryset(concept, user=None):
    q = concept.issues.filter(comicvine_status='MATCHED').order_by('cover_date', 'volume__name',
                                                                   'volume__start_year', 'numerical_number',
                                                                   'number') \
        .annotate(
        parent_slug=Value(concept.slug),
        badge_name=Concat(
            F('volume__name'), Value(' ('), F('volume__start_year'), Value(') #'), F('number'), Value(' '), F('name'),
            output_field=TextField()
        ),
        group_breaker=Func(F('cover_date'), Value('Month YYYY'), function='to_char', output_field=TextField()),
        desc=F('cover_date')
    )
    if user and user.is_authenticated:
        q = q.annotate(finished_flg=Count('finished_users', distinct=True, filter=Q(finished_users=user)))
    return q


def get_volumes_queryset(concept):
    return Volume.objects.filter(
        issues__in=concept.issues.all()
    ).filter(comicvine_status='MATCHED').annotate(
        issues_count=Count('issues'),
        badge_name=Concat(F('name'), Value(' ('), F('start_year'), Value(')'),
                          output_field=TextField()),
        group_breaker=F("start_year"),
        desc=Concat(F('issues_count'), Value(' issue(s)'), output_field=TextField())
    ).order_by('start_year', 'name', 'id')
