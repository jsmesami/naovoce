import os
from uuid import uuid4

from django.conf import settings
from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from sorl.thumbnail import ImageField

from utils.models import TimeStampedModel

from .managers import GalleryManager


class Image(TimeStampedModel):
    def _upload_to(self, filename):
        return 'gallery/{ct}/{id}/{file}'.format(
            ct=self.gallery_ct.model,
            id=self.gallery_id,
            file=self._mangle_name(filename),
        )

    image = ImageField(_('image'), upload_to=_upload_to)
    caption = models.CharField(_('caption'), max_length=140, blank=True)

    gallery_ct = models.ForeignKey(ContentType)
    gallery_id = models.PositiveIntegerField()
    gallery = generic.GenericForeignKey('gallery_ct', 'gallery_id')

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('author'),
        related_name='images',
        blank=True, null=True,
    )

    def is_owner(self, user):
        return self.author.is_active and (self.author == user)

    @staticmethod
    def _mangle_name(filename):
        return uuid4().hex + os.path.splitext(filename)[1]

    def __str__(self):
        filename, ext = os.path.splitext(os.path.basename(self.image.path))
        return filename+ext if len(filename) < 19 else '...{}'.format(filename[-16:]+ext)

    class Meta:
        ordering = '-created',
        verbose_name = _('image')
        verbose_name_plural = _('images')


class GalleryModel(models.Model):
    images = generic.GenericRelation(
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
        image = self.cover_image or self.images.first()
        return image.image if image else None

    class Meta:
        abstract = True
