import re

from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()


_PREPOS_RE = re.compile(r'(?<= |\u00a0)([kosuvzia]) ', re.M | re.I | re.U)


@register.filter
@stringfilter
def prepos(text):
    """
    Append nbsp after on-letter prepositions, so that they wrap.
    """
    return _PREPOS_RE.sub('\g<1>\u00a0', text)
