from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from utils import logging
from utils.view_mixins import (
    ActiveMenuMixin,
    BreadcrumbMixin,
    ElidedPagesPaginatorMixin,
    OnlyWithIssuesMixin,
    OrderingMixin,
)

from .models import Team

logger = logging.getLogger(__name__)


@logging.methods_logged(logger, ['get', ])
class TeamsListView(ElidedPagesPaginatorMixin, ActiveMenuMixin, OnlyWithIssuesMixin, OrderingMixin, BreadcrumbMixin,
                    ListView):
    context_object_name = "teams"
    template_name = "teams/list.html"
    breadcrumb = [{'url': reverse_lazy("teams:list"), 'text': 'Teams'}]
    paginate_by = 48
    possible_order = ('issue_count', '-issue_count', 'volume_count', '-volume_count', 'name', '-name')
    default_ordering = '-issue_count'
    queryset = Team.objects.was_matched().annotate(
        volume_count=Count('issues__volume', distinct=True)
    ).annotate(
        issue_count=Count('issues', distinct=True)
    ).select_related('publisher')
    active_menu_item = 'teams'


teams_list_view = TeamsListView.as_view()


class TeamDetailView(BreadcrumbMixin, DetailView):
    model = Team
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "team"
    template_name = "teams/detail.html"


team_detail_view = TeamDetailView.as_view()
