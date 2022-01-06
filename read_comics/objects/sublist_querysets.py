from django.db.models import Count, F, Q, TextField, Value
from django.db.models.functions import Concat

from read_comics.volumes.models import Volume


def get_issues_queryset(obj, user=None):
    q = obj.issues.filter(comicvine_status='MATCHED').order_by('cover_date', 'volume__name', 'volume__start_year',
                                                               'numerical_number', 'number') \
        .annotate(
        parent_slug=Value(obj.slug),
        badge_name=Concat(
            F('volume__name'), Value(' ('), F('volume__start_year'), Value(') #'), F('number'), Value(' '), F('name'),
            output_field=TextField()
        ),
        desc=F('cover_date')
    )
    if user and user.is_authenticated:
        q = q.annotate(finished_flg=Count('finished_users', distinct=True, filter=Q(finished_users=user)))
    return q


def get_volumes_queryset(obj):
    return Volume.objects.filter(comicvine_status='MATCHED').filter(
        issues__in=obj.issues.all()
    ).annotate(
        issues_count=Count('issues'),
        badge_name=Concat(F('name'), Value(' ('), F('start_year'), Value(')'),
                          output_field=TextField()),
        desc=Concat(F('issues_count'), Value(' issue(s)'), output_field=TextField())
    ).order_by('-issues_count')
