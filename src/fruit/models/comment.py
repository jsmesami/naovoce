from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from utils.models import TimeStampedModel


class Comment(TimeStampedModel):
    text = models.CharField(_('comment'), max_length=1600)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('author'),
        related_name='comments',
        on_delete=models.CASCADE,
    )
    ip = models.GenericIPAddressField(_("author's IP address"), null=True)
    is_complaint = models.BooleanField(_('complaint'), default=False)
    is_rejected = models.BooleanField(_('rejected'), default=False)

    fruit = models.ForeignKey('fruit.Fruit', related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return 'Comment #{pk} by {username}'.format(pk=self.pk, username=self.author.username)

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
        ordering = '-created',
