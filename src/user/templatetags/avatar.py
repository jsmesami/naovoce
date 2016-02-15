from django.template import Library

from utils.avatar import get_avatar

register = Library()


@register.simple_tag(takes_context=True)
def avatar(context, user, requested_size=None, bg_shade=0):
    return get_avatar(context['request'], user, requested_size, bg_shade)
