from rest_framework import serializers
from rest_framework.reverse import reverse

from .serializers import ImageSerializer


class HyperlinkedGalleryField(serializers.HyperlinkedIdentityField):

    def __init__(self, gallery_ct, **kwargs):
        self.gallery_ct = gallery_ct
        # only galleries referenced by this field can contain new images
        ImageSerializer.gallery_ct_whitelist.update([gallery_ct])

        super().__init__('api:image-list', **kwargs)

    def get_url(self, obj, view_name, request, format):
        kwargs = dict(
            gallery_ct=self.gallery_ct,
            gallery_id=obj.pk,
        )
        return reverse(view_name, kwargs=kwargs, request=request, format=format)
