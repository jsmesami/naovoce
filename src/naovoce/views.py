from collections import defaultdict

from django.shortcuts import render

from blog.models import BlogPost
from fruit.models import Kind, Fruit
from comments.models import Comment


def home_view(request):
    fruits_qs = Fruit.objects.valid()\
        .order_by('-created')\
        .select_related('kind', 'user')

    comm_qs = Comment.objects\
        .order_by('-created')\
        .prefetch_related('author', 'content_object')[:6]

    desc_qs = fruits_qs.exclude(description='')[:6]

    comm = [
        dict(
            url=c.get_absolute_url(),
            author=c.author.get_short_name(),
            author_url=c.author.get_absolute_url(),
            text=c.text,
            time=c.created,
        )
        for c in comm_qs
    ]

    desc = [
        dict(
            url=d.get_absolute_url(),
            author=d.user.get_short_name(),
            author_url=d.user.get_absolute_url(),
            text=d.description,
            time=d.created,
        )
        for d in desc_qs
    ]

    context = {
        'blogposts': BlogPost.objects.public(),
        'fruits': fruits_qs,
        'comments': sorted(comm+desc, key=lambda x: x['time'], reverse=True)
    }

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
