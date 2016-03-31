from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from utils.api.permissions import IsOwnerOrReadOnly
from .serializers import ImageSerializer
from ..models import Image


class ImageDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retreive, update or destroy specific Image resource.
    """
    queryset = Image.objects.select_related('author')
    serializer_class = ImageSerializer
    permission_classes = IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly


class ImageList(generics.ListCreateAPIView):
    """
    List or create Image resources.
    """
    serializer_class = ImageSerializer
    permission_classes = IsAuthenticatedOrReadOnly,

    def perform_create(self, serializer):
        gallery_ct = self.kwargs['gallery_ct']
        if gallery_ct not in serializer.gallery_ct_whitelist:
            raise ValidationError(_('Content type {ct} is not supported.').format(
                ct=gallery_ct,
            ))
        # Future caveat:
        # Querying ContentType only by model name will not work, if there is another
        # model of the same name within a different app.
        kwargs = {
            'gallery_ct': ContentType.objects.get(model=gallery_ct),
            'gallery_id': self.kwargs['gallery_id'],
            'author': self.request.user,
        }
        serializer.save(**kwargs)

    def get_queryset(self):
        gallery_ct = self.kwargs.get('gallery_ct')
        gallery_id = self.kwargs.get('gallery_id')

        if gallery_ct not in ImageSerializer.gallery_ct_whitelist:
            raise ValidationError(_('Content type {ct} is not supported.').format(
                ct=gallery_ct,
            ))

        return Image.objects.filter(gallery_ct__model=gallery_ct, gallery_id=gallery_id)
