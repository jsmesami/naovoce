from django.template import Library
from django.utils.text import Truncator
from django.utils.translation import ugettext_lazy as _


register = Library()


@register.simple_tag
def read_more(text, length, target):
    a = ' ... <a href="{url}" class="read-more">{text} &raquo;</a>'

    return Truncator(text).words(
        int(length),
        html=True,
        truncate=a.format(url=target, text=_('Read more')),
    )
