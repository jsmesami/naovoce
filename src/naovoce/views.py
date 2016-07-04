from collections import defaultdict

from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render

from blog.models import BlogPost
from fruit.models import Kind, Fruit
from gallery.models import Image
from user.utils import pickers_counts_context

def latest_images_for_existing_fruit():
    existing_fruits = Fruit.objects.filter(deleted=False).values_list('id', flat=True)
    return Image.objects.filter(gallery_ct=ContentType.objects.get_for_model(Fruit), gallery_id__in=existing_fruits)

def home_view(request):
    context = {
        'blogposts': BlogPost.objects.public(),
        'fruit': Fruit.objects.valid().order_by('-created').select_related('kind', 'user'),
        'images': latest_images_for_existing_fruit(),
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
