from django import template
from utils import utils

register = template.Library()


@register.simple_tag(takes_context=True)
def url_add_query_params(context, **kwargs):
    """
    Adds or replaces query parameters in current url

    :param context: Context
    :param kwargs: query parameters to be added or replaced in url
    :return: url with added or replaces query parameters
    """
    return utils.url_add_query_params(context.request.path, context.request.GET, **kwargs)
