from django.core.paginator import Paginator


def url_add_query_params(base_url, get, **kwargs):
    """
    Adds or replaces query parameters in current url

    :param base_url: base url from request
    :param get: current get parameters
    :param kwargs: query parameters to be added or replaced in url
    :return: url with added or replaces query parameters
    """
    url = base_url
    get_parameters = {k: v for k, v in get.items()}
    if kwargs:
        get_parameters.update(kwargs)
    get_string = '&'.join([f'{k}={v}' for k, v in get_parameters.items()])
    if get_string:
        url += '?' + get_string
    return url


def get_elided_pages_list(page):
    return [
        {'num': x, 'disabled': ('disabled' if x == '…' else ''), 'active': ('active' if x == page.number else '')}
        for x in page.paginator.get_elided_page_range(page.number)
    ]


def get_first_page(context_name, queryset):
    context = {}
    pages = Paginator(
        queryset,
        30
    )
    context[f'{context_name}_first_page'] = pages.page(1)
    context[f'{context_name}_pages'] = get_elided_pages_list(pages.page(1))
    return context


class WrappedQuerySet:

    @staticmethod
    def wrapper(obj):
        raise NotImplementedError

    def __init__(self, queryset):
        self._queryset = queryset
        self._iter = None

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.wrapper(self._queryset[item])
        if isinstance(item, slice):
            return self.__class__(self._queryset.__getitem__(item))
        raise IndexError(item)

    def __len__(self):
        return self._queryset.count()

    def __iter__(self):
        self._iter = iter(self._queryset)
        return self

    def __next__(self):
        try:
            return self.wrapper(next(self._iter))
        except StopIteration:
            raise StopIteration
