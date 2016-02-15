import random
import re

from django.utils.encoding import force_str
from django.utils.safestring import mark_safe
from django.template.base import Library
from django.conf import settings
from django.template.defaultfilters import stringfilter

from sorl.thumbnail import get_thumbnail
from sorl.thumbnail.templatetags.thumbnail import is_portrait

from gallery.models import Image


register = Library()


@register.simple_tag(takes_context=True)
@register.assignment_tag(takes_context=True, name='cache_thumb')
def get_thumb(context, img, w=None, h=None):

    if not img:
        # we must provide path to a static file as a fully qualified external,
        # because sorl.thumbnail forces MEDIA_URL to be the one true source
        img = context['request'].build_absolute_uri(
            '{static}img/holder_{choice}.png'.format(
                static=settings.STATIC_URL,
                choice=random.choice(['01', '02', '03']),
            )
        )

    assert w or h
    h = h or w
    size = '{w}{h}'.format(w=w * 2 if w else '', h='x' + str(h * 2))

    options = dict(
        # crop 20% to the top if size is landscape or square and source is portrait
        crop='20%' if w >= h and is_portrait(img) else 'center',
        quality=40,
        format='JPEG',
        upscale=True,
    )

    return get_thumbnail(img, size, **options).url


_IMG_TAG_RE = re.compile(r'\[\s*IMG(\s+\d+)+\s*\]', re.UNICODE)
_IMG_PKS_RE = re.compile(r'(\d+)')


@register.simple_tag(takes_context=True)
def text_with_thumbs(context, text, w=None, h=None):

    def img_tag_replace(match):
        # get list of primary keys:
        pks = [int(pk) for pk in _IMG_PKS_RE.findall(match.group(0))]
        images = Image.objects.filter(pk__in=pks).values_list('image', 'caption', 'id')
        # sort qs to maintain pks order:
        images = sorted(images, key=lambda i: pks.index(i[2]))

        return '<div class="row thumbs">{images}</div>'.format(
            images=''.join(
                '<img src="{src}" alt="{alt}">'.format(
                    src=get_thumb(context, image, w, h),
                    alt=caption
                ) for (image, caption, pk) in images
            )
        )

    return mark_safe(_IMG_TAG_RE.sub(img_tag_replace, force_str(text)))


@register.filter
@stringfilter
def strip_thumbs(text):
    return _IMG_TAG_RE.sub('', text)
