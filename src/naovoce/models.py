import os

from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.models import TimeStampedModel


class Upload(TimeStampedModel):
    file = models.FileField(_('file'), upload_to='uploads')
    title = models.CharField(_('title'), max_length=255, blank=True,
                             help_text=_('You can assign a title for future reference.'))

    class Meta:
        verbose_name = _('upload')
        verbose_name_plural = _('uploads')
        ordering = '-created',

    def __str__(self):
        return os.path.basename(self.file.path)
