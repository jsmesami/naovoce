from django import template

from ..full_url import get_full_url

register = template.Library()


@register.simple_tag(takes_context=True)
def full_url(context, location):
    return get_full_url(context['request'], location)
