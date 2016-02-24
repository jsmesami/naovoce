from django.conf import settings
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from utils.models import TimeStampedModel


class Comment(TimeStampedModel):
    text = models.CharField(_('comment'), max_length=1600)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('author'))
    ip = models.GenericIPAddressField(_("author's IP address"), null=True)
    complaint = models.BooleanField(_('complaint'), default=False)
    rejected = models.BooleanField(_('rejected'), default=False)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def get_absolute_url(self):
        return '{url}#{anchor}'.format(
            url=self.content_object.get_absolute_url(),
            anchor=self.anchor,
        )

    @cached_property
    def anchor(self):
        return 'comment{}'.format(self.pk)

    def __str__(self):
        return 'Comment #{c.id} by {c.author.username}'.format(c=self)

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
        ordering = '-created',
