from collections import defaultdict
from itertools import chain
from operator import attrgetter

from django.shortcuts import render

from blog.models import BlogPost
from fruit.models import Kind, Fruit
from user.utils import pickers_counts_context


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
