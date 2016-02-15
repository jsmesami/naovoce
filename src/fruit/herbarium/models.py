from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _


class Herbarium(models.Model):
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

    def get_absolute_url(self):
        return reverse('herbarium:detail', args=[self.id, self.slug])

    def __str__(self):
        return self.full_name or self.kind.name

    class Meta:
        app_label = 'fruit'
        verbose_name = _('herbarium item')
        verbose_name_plural = _('herbarium items')
