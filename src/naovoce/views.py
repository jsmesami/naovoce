from collections import defaultdict

from django.shortcuts import render
from fruit.models import Fruit, Kind


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
        'catalogue': Fruit.CATALOGUE,
    }

    return render(request, 'map.html', context)
