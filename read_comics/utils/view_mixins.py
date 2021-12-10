from typing import Optional

from django.contrib.auth.mixins import UserPassesTestMixin
from utils.utils import EndlessPaginator, get_elided_pages_list


class IsAdminMixin(UserPassesTestMixin):
    def test_func(self) -> Optional[bool]:
        return self.request.user.is_staff or self.request.user.is_superuser


class BreadcrumbMixin:
    breadcrumb = []

    def get_context_data(self, **kwargs):
        context = super(BreadcrumbMixin, self).get_context_data(**kwargs)
        context['breadcrumb'] = self.get_breadcrumb()
        return context

    def get_breadcrumb(self):
        if self.breadcrumb:
            return self.breadcrumb
        else:
            return []


class OrderingMixin:
    possible_order = None
    default_ordering = None
    base_queryset = None

    def get_queryset(self):
        q = super(OrderingMixin, self).get_queryset()
        ordering_field = None
        if isinstance(self.possible_order, tuple) or isinstance(self.possible_order, list):
            ordering_field = self.request.GET.get('ordering', self.default_ordering)
            if ordering_field not in self.possible_order:
                ordering_field = None

        if isinstance(self.possible_order, dict):
            ordering_field = self.possible_order.get(self.request.GET.get('ordering'))

        if ordering_field is None:
            ordering_field = self.default_ordering

        if isinstance(ordering_field, str):
            q = q.order_by(ordering_field)
        else:
            q = q.order_by(*ordering_field)
        return q


class OnlyWithIssuesMixin:
    def get_queryset(self):
        q = super(OnlyWithIssuesMixin, self).get_queryset()
        only_with_issues = self.request.GET.get('only-with-issues', 'yes')
        if only_with_issues == 'yes':
            q = q.filter(issue_count__gt=0)
        return q

    def get_context_data(self, **kwargs):
        context = super(OnlyWithIssuesMixin, self).get_context_data(**kwargs)
        context['only_with_issues'] = self.request.GET.get('only-with-issues', 'yes')
        return context


class ActiveMenuMixin:
    active_menu_item = None

    def get_context_data(self, **kwargs):
        context = super(ActiveMenuMixin, self).get_context_data(**kwargs)
        if self.active_menu_item:
            context[self.active_menu_item + '_menu_active'] = True
        return context


class ElidedPagesPaginatorMixin:
    paginator_class = EndlessPaginator

    def get_context_data(self, **kwargs):
        context = super(ElidedPagesPaginatorMixin, self).get_context_data(**kwargs)
        page = context['page_obj']
        context['pages'] = get_elided_pages_list(page)
        return context
