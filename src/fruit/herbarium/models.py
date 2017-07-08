from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from utils.fields import MonthsField


class Herbarium(models.Model):
    """
    Additional information about mapped plants.
    """
    kind = models.OneToOneField('fruit.Kind', verbose_name=_('kind'))

    full_name = models.CharField(_('full name'), max_length=255, blank=True)
    latin_name = models.CharField(_('latin name'), max_length=255, blank=True)
    description = models.TextField(_('description'), blank=True)
    photo = models.ImageField(
        _('photo'),
        upload_to='herbarium',
        blank=True,
        null=True,
        help_text=_('Illustrational photo'),
    )

    @property
    def slug(self):
        return slugify(str(self))

    def __str__(self):
        return self.full_name or self.kind.name

    class Meta:
        app_label = 'fruit'
        verbose_name = _('herbarium item')
        verbose_name_plural = _('herbarium items')


class Season(models.Model):
    """
    Season during which a specified part of a plant is ripening. Note that this is undocumented
    feature, which is here only to appease mobile app developers' requirement.
    The model currently does not support _locations_ in favor of simplicity - this shortcoming
    shoud be adressed when (and if) the target audience exceeds borders of Czechoslovakia.
    """
    herb = models.ForeignKey(Herbarium, verbose_name=_('herbarium item'), related_name='seasons')

    part = models.CharField(_('ripening plant part'), max_length=255)

    start = MonthsField(
        _('ripening start'),
        help_text=_('Month when specified plant part ripening starts.'),
    )
    duration = MonthsField(
        _('ripening duration'),
        help_text=_('Duration of ripening in months.'),
    )

    class Meta:
        app_label = 'fruit'
        unique_together = 'part', 'herb'
        verbose_name = _('ripening season')
        verbose_name_plural = _('ripening seasons')
