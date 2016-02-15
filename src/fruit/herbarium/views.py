from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, render

from fruit.models import Kind
from .models import Herbarium


def index(request, cls=None, slug=None):
    context = {
        'classes': Kind.CLS.choices,
    }

    herbs = Herbarium.objects.select_related('kind')
    if cls:
        cls_ids = [i for i, name in Kind.CLS.choices]
        cls = int(cls)
        if cls not in cls_ids:
            raise Http404
        else:
            cls_slug = Kind.cls_slug(cls)
            if cls_slug != slug:
                return HttpResponsePermanentRedirect(
                    reverse('herbarium:filter', args=[cls, cls_slug])
                )

            herbs = herbs.filter(kind__cls=cls)
            context['filter'] = cls

    context['index'] = herbs
    return render(request, 'fruit/herbarium.html', context)


def detail(request, pk, slug=None):
    item = get_object_or_404(Herbarium.objects.select_related('kind'), pk=pk)
    if item.slug != slug:
        return HttpResponsePermanentRedirect(item.get_absolute_url())

    return render(request, 'fruit/herbarium.html', {'detail': item})
