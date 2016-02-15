import utils

from django.template import Library

register = Library()


@register.filter
def naturalsort(objects, key=None):
    return utils.naturalsort(objects, key)
