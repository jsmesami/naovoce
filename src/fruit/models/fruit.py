from django.contrib.gis.db.models import PointField
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.choices import Choices
from utils.models import TimeStampedModel


class ValidFruitQuerySet(models.QuerySet):
    def valid(self):
        return self.exclude(deleted=True)


class Fruit(TimeStampedModel):
    position = PointField(_('position'), null=True, blank=True, srid=4326)
    kind = models.ForeignKey(
        'fruit.Kind',
        verbose_name=_('kind'),
        related_name='fruits',
        on_delete=models.CASCADE,
    )
    CATALOGUE = Choices(
        naovoce=(1000, 'naovoce'),
        revival=(2000, _('revival')),
    )
    catalogue = models.IntegerField(
        _('resolution'),
        choices=CATALOGUE.choices,
        default=CATALOGUE.naovoce,
    )

    description = models.TextField(
        _('description'),
        blank=True,
        help_text=_('Please, provide as many information about the marker as you find relevant.')
    )

    deleted = models.BooleanField(_('deleted'), default=False, db_index=True)
    why_deleted = models.TextField(
        _('why deleted'),
        blank=True,
        help_text=_('The tree has been cut down, not found etc.'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user'),
        related_name='fruits',
        on_delete=models.CASCADE,
    )

    objects = models.Manager.from_queryset(ValidFruitQuerySet)()

    def is_owner(self, user):
        return self.user.is_active and (self.user == user)

    def __str__(self):
        return '{fruit.kind!s}'.format(fruit=self)

    class Meta:
        verbose_name = _('fruit')
        verbose_name_plural = _('fruit')
