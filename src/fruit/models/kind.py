import random

from django.db import models
from django.utils.translation import ugettext_lazy as _
from utils.choices import Choices


def _get_random_key():
    """Choose random key from Yi syllables Unicode range."""

    return '{key:x}'.format(
        key=random.randint(0xA000, 0xA48C)
    )


class Kind(models.Model):

    CLS = Choices(
        tree=(1000, _('Trees')),
        bush=(2000, _('Bushes')),
        herb=(3000, _('Herbs')),
        nut=(4000, _('Nuts')),
    )

    cls = models.IntegerField(_('class'), choices=CLS.choices)
    name = models.CharField(_('name'), max_length=255, unique=True)
    color = models.CharField(
        _('color'),
        max_length=6,
        default='AAFF32',
        help_text=_('Hex color triplet for map.'),
    )
    key = models.CharField(
        _('key'),
        unique=True,
        max_length=4,
        default=_get_random_key,
        help_text=_('ID for API and also index in the markers font')
    )

    @property
    def cls_name(self):
        return Kind.CLS.text_of(self.cls)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('kind')
        verbose_name_plural = _('kinds')
        ordering = 'cls', 'name'
