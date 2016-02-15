import base64
import imghdr

from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import ContentFile

from rest_framework import serializers
from rest_framework.reverse import reverse

from user.api.serializers import UserSerializer
from ..models import Image


class Base64ImageField(serializers.ImageField):
    """
    This field allows uploading an image either as a raw POST data or
    Base64-encoded string within a json payload.
    """
    def to_internal_value(self, data):
        # If data is a string, try to base64-decode it.
        if isinstance(data, str):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')

            try:
                decoded_data = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            file_name = 'uploaded_image.'+self.guess_file_extension(decoded_data)

            data = ContentFile(decoded_data, name=file_name)

        return super().to_internal_value(data)

    def guess_file_extension(self, image_data):
        extension = imghdr.what(None, image_data)
        return extension.lower() if extension else 'jpg'


class ImageSerializer(serializers.HyperlinkedModelSerializer):

    # whitelist of content types, automatically updated when
    # HyperlinkedGalleryField is instantiated
    gallery_ct_whitelist = set()

    image = Base64ImageField()

    author = UserSerializer(read_only=True)

    class Meta:
        model = Image
        fields = 'id image caption author'.split()


class HyperlinkedGalleryField(serializers.HyperlinkedIdentityField):

    view_name = 'api:image-list'

    def __init__(self, **kwargs):
        gallery_ct = kwargs.pop('gallery_ct')
        if not gallery_ct:
            raise ImproperlyConfigured('The `gallery_ct` argument is required.')

        self.gallery_ct = gallery_ct
        # only galleries referenced by this field can contain new images
        ImageSerializer.gallery_ct_whitelist.update([gallery_ct])

        super().__init__(self.view_name, **kwargs)

    def get_url(self, obj, view_name, request, format):
        kwargs = dict(
            gallery_ct=self.gallery_ct,
            gallery_id=obj.pk,
        )
        return reverse(self.view_name, kwargs=kwargs, request=self.context['request'])
