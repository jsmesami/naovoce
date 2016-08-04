import os

from django.db import models
from django.utils.functional import cached_property
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from utils.choices import Choices
from utils.models import TimeStampedModel


class Upload(TimeStampedModel):
    """
    Arbitrary file uploads (like annual reports or press releases)
    """
    file = models.FileField(_('file'), upload_to='uploads')
    title = models.CharField(_('title'), max_length=255, blank=True,
                             help_text=_('You can assign a title for future reference.'))

    class Meta:
        verbose_name = _('upload')
        verbose_name_plural = _('uploads')
        ordering = '-created',

    def __str__(self):
        return os.path.basename(self.file.path)


class Media(models.Model):
    """
    Stores media coverage to be bragged-about.
    """
    TYPE = Choices(
        online=(1000, _('Online media')),
        printed=(2000, _('Printed media')),
        broadcast=(3000, _('TV / Radio')),
    )

    name = models.CharField(_('name'), max_length=255)
    date = models.DateField(_('date published'))
    logo = models.FileField(_('logo'), upload_to='partners/logos')
    type = models.IntegerField(_('type'), choices=TYPE.choices, default=TYPE.online)

    title = models.CharField(_('title'), max_length=255, blank=True)
    perex = models.TextField(_('perex'), blank=True)
    link = models.URLField(_('link'), blank=True)

    @cached_property
    def type_slug(self):
        return slugify(self.TYPE.text_of(self.type))

    class Meta:
        verbose_name = _('media')
        verbose_name_plural = _('media')
        ordering = '-date',

    def __str__(self):
        return self.title
