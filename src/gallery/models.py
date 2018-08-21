import os
from uuid import uuid4

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from utils.fields import ContentTypeRestrictedImageField
from utils.models import TimeStampedModel

from .settings import GALLERY_PUBLIC_CONTAINERS, GALLERY_IMAGE_MAX_FILESIZE
from .managers import GalleryManager


class Image(TimeStampedModel):
    def _upload_to(self, filename):
        return 'gallery/{ct}/{id}/{file}'.format(
            ct=self.gallery_ct.model,
            id=self.gallery_id,
            file=self._mangle_name(filename),
        )

    image = ContentTypeRestrictedImageField(
        _('image'),
        upload_to=_upload_to,
        content_types=['image/jpeg'],
        max_upload_size=GALLERY_IMAGE_MAX_FILESIZE
    )

    caption = models.CharField(_('caption'), max_length=140, blank=True)

    gallery_ct = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )
    gallery_id = models.PositiveIntegerField()
    gallery = GenericForeignKey('gallery_ct', 'gallery_id')

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('author'),
        related_name='images',
        blank=True, null=True,
        on_delete=models.CASCADE,
    )

    def is_owner(self, user):
        return self.author.is_active and (self.author == user)

    @staticmethod
    def _mangle_name(filename):
        return uuid4().hex + os.path.splitext(filename)[1]

    def get_absolute_url(self):
        return reverse('gallery:browser', args=[self.gallery_ct.model, self.gallery_id, self.id])

    def __str__(self):
        filename, ext = os.path.splitext(os.path.basename(self.image.path))
        return filename + ext if len(filename) < 19 else '...{}'.format(filename[-16:] + ext)

    class Meta:
        ordering = '-created',
        verbose_name = _('image LEGACY')
        verbose_name_plural = _('images LEGACY')


class GalleryModel(models.Model):
    images = GenericRelation(
        Image,
        verbose_name=_('images'),
        content_type_field='gallery_ct',
        object_id_field='gallery_id',
    )

    cover_image = models.ForeignKey(
        Image,
        verbose_name=_('cover image'),
        blank=True,
        null=True,
        related_name='+',
        on_delete=models.SET_NULL,
    )

    objects = GalleryManager()

    def get_cover_image(self):
        image = self.cover_image or self.images.order_by('created').first()
        return image or None

    @cached_property
    def images_index_url(self):
        gallery_ct = ContentType.objects.get_for_model(self)
        return reverse('gallery:index', args=[gallery_ct.model, self.id])

    def is_gallery_public(self):
        return self.__class__.__name__.lower() in GALLERY_PUBLIC_CONTAINERS

    class Meta:
        abstract = True
