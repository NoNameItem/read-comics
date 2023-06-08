from rest_framework.filters import OrderingFilter


class UniqueOrderingFilter(OrderingFilter):
    def get_ordering(self, request, queryset, view):
        ordering = super().get_ordering(request, queryset, view)
        return [*(ordering or []), "id"]
