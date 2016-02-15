from django.db import models
from django.utils.translation import ugettext_lazy as _


class StaticPage(models.Model):
    url = models.CharField('URL', max_length=50, unique=True)

    title = models.CharField(_('title'), max_length=50)
    text = models.TextField(_('text'), blank=True)
    meta_description = models.CharField(_('meta description'), max_length=150, blank=True)

    class Meta:
        verbose_name = _('static page')
        verbose_name_plural = _('static pages')

    def __unicode__(self):
        return '{page.title}: {page.url}'.format(page=self)

    def get_absolute_url(self):
        return self.url
