from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from utils.view_mixins import ElidedPagesPaginatorMixin


class BaseSublistView(ElidedPagesPaginatorMixin, ListView):
    template_name = "blocks/detail/badges.html"
    context_object_name = 'objects'
    paginate_by = 30
    get_queryset_func = None
    parent_model = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.obj = None

    def get_queryset(self):
        self.obj = get_object_or_404(self.parent_model, slug=self.kwargs.get('slug'))
        return self.get_queryset_func(self.obj)
