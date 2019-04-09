import os
from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from utils.models import TimeStampedModel


class Image(TimeStampedModel):
    def _upload_to(self, filename):
        mangled_name = uuid4().hex + os.path.splitext(filename)[1]

        return 'fruit/{id}/images/{file}'.format(
            id=self.fruit_id,
            file=mangled_name,
        )

    image = models.ImageField(_('image'), upload_to=_upload_to)

    caption = models.CharField(_('caption'), max_length=280, blank=True)

    fruit = models.ForeignKey('fruit.Fruit', related_name='images', on_delete=models.CASCADE)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('author'),
        related_name='images',
        blank=True, null=True,
        on_delete=models.CASCADE,
    )

    def is_owner(self, user):
        return self.author == user

    def __str__(self):
        filename, ext = os.path.splitext(os.path.basename(self.image.path))
        return filename + ext if len(filename) < 19 else '...{}'.format(filename[-16:] + ext)

    class Meta:
        ordering = ('-created',)
        verbose_name = _('image')
        verbose_name_plural = _('images')