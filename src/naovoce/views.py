from collections import defaultdict
from itertools import chain
from operator import attrgetter

from django.http.response import Http404
from django.shortcuts import render
from django.utils.text import slugify

from blog.models import BlogPost
from fruit.models import Kind, Fruit
from user.utils import pickers_counts_context

from .models import Media


def get_latest_images(qs, limit):
    img_sets = (f.images.all() for f in qs.exclude(images=None)[:limit])
    return list(reversed(sorted(chain.from_iterable(img_sets), key=attrgetter('created'))))[:limit]


def home_view(request):
    fruit_qs = Fruit.objects.valid().order_by('-created').select_related('kind', 'user')

    context = {
        'blogposts': BlogPost.objects.public(),
        'fruit': fruit_qs,
        'images': get_latest_images(fruit_qs, limit=7),
    }

    context.update(pickers_counts_context())

    return render(request, 'home.html', context)


def map_view(request):
    kinds = Kind.objects.all()

    kinds_by_class = defaultdict(list)
    for k in kinds:
        kinds_by_class[Kind.CLS.name_of(k.cls)].append(k)

    classes = [(Kind.CLS.name_of(num), text) for num, text in Kind.CLS.choices]

    context = {
        'kinds': kinds,
        'kinds_by_class': kinds_by_class,
        'classes': classes,
    }

    return render(request, 'map.html', context)


def media_view(request, type_slug=None):

    if not type_slug:
        media_qs = Media.objects.all()
    else:
        try:
            media_type_indexes = {slugify(text): index for index, text in Media.TYPE.choices}
            media_qs = Media.objects.filter(type=media_type_indexes[type_slug])
        except KeyError:
            return Http404()

    context = {
        'media': media_qs,
        'media_types': ((text.lower(), slugify(text)) for index, text in Media.TYPE.choices),
        'active_type_slug': type_slug,
    }

    return render(request, 'media.html', context)
