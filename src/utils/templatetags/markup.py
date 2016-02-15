import markdown2

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_str
from django.utils.safestring import mark_safe


parser = markdown2.Markdown(safe_mode=False)

register = template.Library()


@register.filter
@stringfilter
def markdown(text):
    return mark_safe(parser.convert(force_str(text)))
