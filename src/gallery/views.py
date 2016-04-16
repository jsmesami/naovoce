from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.views.generic import View
from django.shortcuts import render

from utils import to_linkedlist
from .utils import get_gallery_context


def get_gallery_object(model, gallery_id):
    try:
        gallery_ct = ContentType.objects.get(model=model)
        return gallery_ct.get_object_for_this_type(id=gallery_id)
    except ObjectDoesNotExist:
        raise Http404


class Index(View):

    template_name = 'gallery/index.html'

    def get(self, request, gallery_ct, gallery_id):
        context = get_gallery_context(request, get_gallery_object(gallery_ct, gallery_id))
        return render(request, self.template_name, context)

    def post(self, request, gallery_ct, gallery_id):
        context = get_gallery_context(request, get_gallery_object(gallery_ct, gallery_id))
        return render(request, self.template_name, context)


class Browser(View):

    template_name = 'gallery/browser.html'

    def get(self, request, gallery_ct, gallery_id, image_id):
        container = get_gallery_object(gallery_ct, gallery_id)

        images = container.images.select_related('author').iterator()
        for prev, current, next in to_linkedlist(images):
            if current.id == int(image_id):
                break
        else:
            raise Http404

        context = {
            'container': container,
            'current': current,
            'prev': prev,
            'next': next,
        }
        return render(request, self.template_name, context)
