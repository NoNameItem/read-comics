import datetime
import json

from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.db.models import Count, Q
from django.http import HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import formats
from django.views.generic import DetailView, ListView
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from utils import logging
from utils.view_mixins import (
    ActiveMenuMixin,
    BreadcrumbMixin,
    ElidedPagesPaginatorMixin,
    OrderingMixin,
)

from read_comics.issues.models import FinishedIssue, Issue

logger = logging.getLogger(__name__)


@logging.methods_logged(logger, ['get', ])
class IssuesListView(ElidedPagesPaginatorMixin, ActiveMenuMixin, OrderingMixin, BreadcrumbMixin, ListView):
    context_object_name = "issues"
    template_name = "issues/list.html"
    breadcrumb = [{'url': reverse_lazy("issues:list"), 'text': 'Issues'}]
    paginate_by = 48
    possible_order = {
        'name': ('volume__name', 'volume__start_year', 'numerical_number', 'number'),
        '-name': ('-volume__name', '-volume__start_year', '-numerical_number', '-number'),
        'cover_date': ('cover_date', 'volume__name', 'volume__start_year', 'numerical_number', 'number'),
        '-cover_date': ('-cover_date', '-volume__name', '-volume__start_year', '-numerical_number', '-number')
    }
    default_ordering = ('cover_date', 'volume', 'volume__start_year', 'number')
    queryset = Issue.objects.matched().select_related('volume', 'volume__publisher')
    active_menu_item = 'issues'

    def get_context_data(self, **kwargs):
        context = super(IssuesListView, self).get_context_data(**kwargs)
        ordering = self.request.GET.get('ordering', 'cover_date')
        if ordering in ('name', '-name'):
            context['breaking'] = 'volume'
        elif ordering in ('cover_date', '-cover_date'):
            context['breaking'] = 'date'
        context['hide_finished'] = self.request.GET.get('hide_finished', 'yes')
        return context

    def get_queryset(self):
        q = super(IssuesListView, self).get_queryset()
        if self.request.user.is_authenticated:
            q = q.annotate(
                finished_flg=Count('finished_users', distinct=True, filter=Q(finished_users=self.request.user)))
            if self.request.GET.get('hide_finished', 'yes') == 'yes':
                q = q.filter(finished_flg=0)
        return q


issues_list_view = IssuesListView.as_view()


# @logging.methods_logged(logger, ['get', ])
class IssueDetailView(ActiveMenuMixin, BreadcrumbMixin, DetailView):
    model = Issue
    queryset = Issue.objects.select_related('volume', 'volume__publisher')
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "issue"
    template_name = "issues/detail.html"
    base_queryset = Issue.objects.matched()
    active_menu_item = 'issues'

    def get_breadcrumb(self):
        issue = self.object

        return [
            {'url': reverse_lazy("issues:list") + "?ordering=" + self.get_ordering(), 'text': 'Issues'},
            {'url': '#',
             'text': f"{issue.get_volume_name()} ({issue.get_volume_start_year()}) #{issue.number}"}
        ]

    def get_context_data(self, **kwargs):
        context = super(IssueDetailView, self).get_context_data(**kwargs)
        issue = self.object

        context['authors'] = [
            {
                'name': x.person.name,
                'desc': x.role,
                'square_avatar': x.person.square_avatar,
                'get_absolute_url': x.person.get_absolute_url()
            }
            for x in issue.authors.select_related('person')]

        if self.request.user.is_authenticated:
            try:
                context['finished'] = issue.finished.get(user=self.request.user)
            except FinishedIssue.DoesNotExist:
                pass

        context['previous_link'] = self.get_previous_link()
        context['next_link'] = self.get_next_link()
        context['number_in_sublist'] = self.get_previous_queryset().count() + 1
        context['total_in_sublist'] = self.base_queryset.count()

        context['first_appearance_characters_count'] = issue.first_appearance_characters.\
            filter(comicvine_status='MATCHED').count()
        context['first_appearance_concepts_count'] = issue.first_appearance_concepts.\
            filter(comicvine_status='MATCHED').count()
        context['first_appearance_objects_count'] = issue.first_appearance_objects.\
            filter(comicvine_status='MATCHED').count()
        context['first_appearance_locations_count'] = issue.first_appearance_locations.\
            filter(comicvine_status='MATCHED').count()
        context['first_appearance_teams_count'] = issue.first_appearance_teams.\
            filter(comicvine_status='MATCHED').count()
        context['first_appearance_count'] = (context['first_appearance_characters_count'] +
                                             context['first_appearance_concepts_count'] +
                                             context['first_appearance_objects_count'] +
                                             context['first_appearance_locations_count'] +
                                             context['first_appearance_teams_count'])

        context['characters_count'] = issue.characters.filter(comicvine_status='MATCHED').count()
        context['characters_died_count'] = issue.characters_died.filter(comicvine_status='MATCHED').count()
        context['concepts_count'] = issue.concepts.filter(comicvine_status='MATCHED').count()
        context['locations_count'] = issue.locations.filter(comicvine_status='MATCHED').count()
        context['objects_count'] = issue.objects_in.filter(comicvine_status='MATCHED').count()
        context['authors_count'] = issue.authors.count()
        context['story_arcs_count'] = issue.story_arcs.filter(comicvine_status='MATCHED').count()
        context['teams_count'] = issue.teams.filter(comicvine_status='MATCHED').count()
        context['disbanded_teams_count'] = issue.disbanded_teams.filter(comicvine_status='MATCHED').count()

        context['characters'] = issue.characters.filter(comicvine_status='MATCHED').all()
        context['characters_died'] = issue.characters_died.filter(comicvine_status='MATCHED').all()
        context['concepts'] = issue.concepts.filter(comicvine_status='MATCHED').all()
        context['locations'] = issue.locations.filter(comicvine_status='MATCHED').all()
        context['objects'] = issue.objects_in.filter(comicvine_status='MATCHED').all()
        # context['authors'] = issue.authors.filter(person__comicvine_status='MATCHED').all()
        context['story_arcs'] = issue.story_arcs.filter(comicvine_status='MATCHED').all()
        context['teams'] = issue.teams.filter(comicvine_status='MATCHED').all()
        context['disbanded_teams'] = issue.disbanded_teams.filter(comicvine_status='MATCHED').all()

        if self.request.user.is_authenticated:
            context['base_total_count'] = self.base_queryset.count()
            context['finished_count'] = self.base_queryset.annotate(
                finished_flg=Count('finished_users', distinct=True, filter=Q(finished_users=self.request.user))
            ).exclude(finished_flg=0).count()
            context['finished_percent'] = context['finished_count'] / context['base_total_count'] * 100
            context['base_object'] = self.base_object

        return context

    def get_ordering(self):
        return self.request.GET.get('ordering', 'cover_date')

    def get_next_link(self):
        issues = self.get_next_queryset()
        if issues.count():
            return self.issue_to_url(issues[:1][0])
        else:
            return None

    # noinspection DuplicatedCode
    def get_next_queryset(self):
        issue = self.object
        ordering = self.get_ordering()
        issues = None
        try:
            if ordering == '-cover_date':
                # ('cover_date', 'volume__name', 'volume__start_year', 'number')
                issues = self.base_queryset.exclude(pk=issue.pk).filter(
                    Q(cover_date__lt=issue.cover_date) |
                    (
                        Q(cover_date=issue.cover_date) &
                        Q(volume__name__lt=issue.volume.name)) |
                    (
                        Q(cover_date=issue.cover_date) &
                        Q(volume__name=issue.volume.name) &
                        Q(volume__start_year__lt=issue.volume.start_year)
                    ) |
                    (
                        Q(cover_date=issue.cover_date) &
                        Q(volume__name=issue.volume.name) &
                        Q(volume__start_year=issue.volume.start_year) &
                        Q(numerical_number__lt=issue.numerical_number)
                    ) |
                    (
                        Q(cover_date=issue.cover_date) &
                        Q(volume__name=issue.volume.name) &
                        Q(volume__start_year=issue.volume.start_year) &
                        Q(numerical_number=issue.numerical_number) &
                        Q(number__lt=issue.number)
                    )
                ).order_by('-cover_date', '-volume__name', '-volume__start_year', '-numerical_number', '-number')
            elif ordering == 'cover_date':
                # ('-cover_date', '-volume', '-volume__start_year', '-number')
                issues = self.base_queryset.exclude(pk=issue.pk).filter(
                    Q(cover_date__gt=issue.cover_date) |
                    (
                        Q(cover_date=issue.cover_date) &
                        Q(volume__name__gt=issue.volume.name)) |
                    (
                        Q(cover_date=issue.cover_date) &
                        Q(volume__name=issue.volume.name) &
                        Q(volume__start_year__gt=issue.volume.start_year)
                    ) |
                    (
                        Q(cover_date=issue.cover_date) &
                        Q(volume__name=issue.volume.name) &
                        Q(volume__start_year=issue.volume.start_year) &
                        Q(numerical_number__gt=issue.numerical_number)
                    ) |
                    (
                        Q(cover_date=issue.cover_date) &
                        Q(volume__name=issue.volume.name) &
                        Q(volume__start_year=issue.volume.start_year) &
                        Q(numerical_number=issue.numerical_number) &
                        Q(number__gt=issue.number)
                    )
                ).order_by('cover_date', 'volume__name', 'volume__start_year', 'numerical_number', 'number')
            elif ordering == 'name':
                # ('-volume__name', '-volume__start_year', '-number')
                issues = self.base_queryset.exclude(pk=issue.pk).filter(
                    Q(volume__name__gt=issue.volume.name) |
                    (
                        Q(volume__name=issue.volume.name) &
                        Q(volume__start_year__gt=issue.volume.start_year)
                    ) |
                    (
                        Q(volume__name=issue.volume.name) &
                        Q(volume__start_year=issue.volume.start_year) &
                        Q(numerical_number__gt=issue.numerical_number)
                    ) |
                    (
                        Q(volume__name=issue.volume.name) &
                        Q(volume__start_year=issue.volume.start_year) &
                        Q(numerical_number=issue.numerical_number) &
                        Q(number__gt=issue.number)
                    )
                ).order_by('volume__name', 'volume__start_year', 'numerical_number', 'number')
            elif ordering == '-name':
                # ('volume__name', 'volume__start_year', 'number')
                issues = self.base_queryset.exclude(pk=issue.pk).filter(
                    Q(volume__name__lt=issue.volume.name) |
                    (
                        Q(volume__name=issue.volume.name) &
                        Q(volume__start_year__lt=issue.volume.start_year)
                    ) |
                    (
                        Q(volume__name=issue.volume.name) &
                        Q(volume__start_year=issue.volume.start_year) &
                        Q(numerical_number__lt=issue.numerical_number)
                    ) |
                    (
                        Q(volume__name=issue.volume.name) &
                        Q(volume__start_year=issue.volume.start_year) &
                        Q(numerical_number=issue.numerical_number) &
                        Q(number__lt=issue.number)
                    )
                ).order_by('-volume__name', '-volume__start_year', '-numerical_number', '-number')
        except ValueError:
            issues = self.base_queryset.none()
        return issues

    def get_previous_link(self):
        issues = self.get_previous_queryset()
        if issues.count():
            return self.issue_to_url(issues[:1][0])
        else:
            return None

    # noinspection DuplicatedCode
    def get_previous_queryset(self):
        issue = self.object
        ordering = self.get_ordering()
        issues = None
        try:
            if ordering == 'cover_date':
                # ('cover_date', 'volume__name', 'volume__start_year', 'number')
                issues = self.base_queryset.exclude(pk=issue.pk).filter(
                    Q(cover_date__lt=issue.cover_date) |
                    (
                        Q(cover_date=issue.cover_date) &
                        Q(volume__name__lt=issue.volume.name)) |
                    (
                        Q(cover_date=issue.cover_date) &
                        Q(volume__name=issue.volume.name) &
                        Q(volume__start_year__lt=issue.volume.start_year)
                    ) |
                    (
                        Q(cover_date=issue.cover_date) &
                        Q(volume__name=issue.volume.name) &
                        Q(volume__start_year=issue.volume.start_year) &
                        Q(numerical_number__lt=issue.numerical_number)
                    ) |
                    (
                        Q(cover_date=issue.cover_date) &
                        Q(volume__name=issue.volume.name) &
                        Q(volume__start_year=issue.volume.start_year) &
                        Q(numerical_number=issue.numerical_number) &
                        Q(number__lt=issue.number)
                    )
                ).order_by('-cover_date', '-volume__name', '-volume__start_year', '-numerical_number', '-number')
            elif ordering == '-cover_date':
                # ('-cover_date', '-volume', '-volume__start_year', '-number')
                issues = self.base_queryset.exclude(pk=issue.pk).filter(
                    Q(cover_date__gt=issue.cover_date) |
                    (
                        Q(cover_date=issue.cover_date) &
                        Q(volume__name__gt=issue.volume.name)) |
                    (
                        Q(cover_date=issue.cover_date) &
                        Q(volume__name=issue.volume.name) &
                        Q(volume__start_year__gt=issue.volume.start_year)
                    ) |
                    (
                        Q(cover_date=issue.cover_date) &
                        Q(volume__name=issue.volume.name) &
                        Q(volume__start_year=issue.volume.start_year) &
                        Q(numerical_number__gt=issue.numerical_number)
                    ) |
                    (
                        Q(cover_date=issue.cover_date) &
                        Q(volume__name=issue.volume.name) &
                        Q(volume__start_year=issue.volume.start_year) &
                        Q(numerical_number=issue.numerical_number) &
                        Q(number__gt=issue.number)
                    )
                ).order_by('cover_date', 'volume__name', 'volume__start_year', 'numerical_number', 'number')
            elif ordering == '-name':
                # ('-volume__name', '-volume__start_year', '-number')
                issues = self.base_queryset.exclude(pk=issue.pk).filter(
                    Q(volume__name__gt=issue.volume.name) |
                    (
                        Q(volume__name=issue.volume.name) &
                        Q(volume__start_year__gt=issue.volume.start_year)
                    ) |
                    (
                        Q(volume__name=issue.volume.name) &
                        Q(volume__start_year=issue.volume.start_year) &
                        Q(numerical_number__gt=issue.numerical_number)
                    ) |
                    (
                        Q(volume__name=issue.volume.name) &
                        Q(volume__start_year=issue.volume.start_year) &
                        Q(numerical_number=issue.numerical_number) &
                        Q(number__gt=issue.number)
                    )
                ).order_by('volume__name', 'volume__start_year', 'numerical_number', 'number')
            elif ordering == 'name':
                # ('volume__name', 'volume__start_year', 'number')
                issues = self.base_queryset.exclude(pk=issue.pk).filter(
                    Q(volume__name__lt=issue.volume.name) |
                    (
                        Q(volume__name=issue.volume.name) &
                        Q(volume__start_year__lt=issue.volume.start_year)
                    ) |
                    (
                        Q(volume__name=issue.volume.name) &
                        Q(volume__start_year=issue.volume.start_year) &
                        Q(numerical_number__lt=issue.numerical_number)
                    ) |
                    (
                        Q(volume__name=issue.volume.name) &
                        Q(volume__start_year=issue.volume.start_year) &
                        Q(numerical_number=issue.numerical_number) &
                        Q(number__lt=issue.number)
                    )
                ).order_by('-volume__name', '-volume__start_year', '-numerical_number', '-number')
        except ValueError:
            issues = self.base_queryset.none()
        return issues

    def issue_to_url(self, issue):
        return issue.get_absolute_url() + f'?ordering={self.get_ordering()}'

    def __init__(self, **kwargs):
        super(IssueDetailView, self).__init__(**kwargs)
        self.base_object = None


issue_detail_view = IssueDetailView.as_view()


class IssueDownloadView(SingleObjectMixin, View):
    queryset = Issue.objects.matched()

    def get(self, request, *args, **kwargs):
        issue = self.get_object()
        return HttpResponseRedirect(issue.download_link)


issue_download_view = IssueDownloadView.as_view()


class IssueMarkFinishedView(LoginRequiredMixin, View):
    def get_total_context(self):
        context = dict()
        if self.request.user.is_authenticated:
            context["total_count"] = Issue.objects.matched().count()
            context["finished_count"] = Issue.objects.matched().annotate(
                finished_flg=Count('finished_users', distinct=True, filter=Q(finished_users=self.request.user))
            ).exclude(finished_flg=0).count()
            context["finished_percent"] = context["finished_count"] / context["total_count"] * 100
        return context

    def get_object_context(self, app_label, model_name, slug):
        context = dict()

        if self.request.user.is_authenticated:
            model = apps.get_model(app_label, model_name)
            obj = model.objects.get(slug=slug)
            context["base_object"] = obj
            context["total_count"] = obj.issues.filter(comicvine_status='MATCHED').count()
            context["finished_count"] = obj.issues.filter(comicvine_status='MATCHED').annotate(
                finished_flg=Count('finished_users', distinct=True, filter=Q(finished_users=self.request.user))
            ).exclude(finished_flg=0).count()
            context["finished_percent"] = context["finished_count"] / context["total_count"] * 100

        return context

    def get_publisher_context(self, slug):
        context = dict()

        if self.request.user.is_authenticated:
            model = apps.get_model("publishers", "Publisher")
            publisher = model.objects.get(slug=slug)
            context["base_object"] = publisher
            context["total_count"] = Issue.objects.filter(comicvine_status='MATCHED').filter(
                volume__publisher=publisher
            ).count()
            context["finished_count"] = Issue.objects.filter(comicvine_status='MATCHED').filter(
                volume__publisher=publisher
            ).annotate(
                finished_flg=Count('finished_users', distinct=True, filter=Q(finished_users=self.request.user))
            ).exclude(finished_flg=0).count()
            context["finished_percent"] = context["finished_count"] / context["total_count"] * 100

        return context

    def get_finished_stats(self):
        payload = json.loads(self.request.body)
        base_object_app_label = payload.get('base_object_app_label')
        base_object_model_name = payload.get('base_object_model_name')
        base_object_slug = payload.get('base_object_slug')
        if base_object_app_label and base_object_model_name and base_object_slug:
            if base_object_app_label == "publishers":
                context = self.get_publisher_context(base_object_slug)
            else:
                context = self.get_object_context(base_object_app_label, base_object_model_name, base_object_slug)
        else:
            context = self.get_total_context()

        return render_to_string("issues/blocks/finished_progress.html", context, request=self.request)

    def post(self, request, slug):
        try:
            issue = Issue.objects.get(slug=slug)
            user = request.user
            issue.finished_users.add(user)
            finished_stats = self.get_finished_stats()

            return JsonResponse({'status': "success", 'issue_name': issue.get_full_name(),
                                 'date': formats.localize(datetime.date.today(), use_l10n=True),
                                 "finished_stats": finished_stats
                                 })
        except IntegrityError:
            return JsonResponse({'status': 'error', 'message': 'You already marked this issue as finished'})
        except Exception as err:
            return JsonResponse({'status': 'error', 'message': 'Unknown error, please contact administrator. \n'
                                                               'Error message: %s' % err.args[0]})


issue_mark_finished_view = IssueMarkFinishedView.as_view()
