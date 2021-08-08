import random

from django.contrib.gis.db.models import PointField
from django.conf import settings
from django.urls import reverse
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from gallery.managers import GalleryManager
from gallery.models import GalleryModel
from utils.choices import Choices
from utils.models import TimeStampedModel


def _get_random_key():
    """
    Chooses random key from Yi syllables Unicode range.
    """
    return '{key:x}'.format(
        key=random.randint(0xA000, 0xA48C)
    )


class ValidKindsQuerySet(models.QuerySet):
    def valid(self):
        return self.exclude(deleted=True)


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
    deleted = models.BooleanField(_('deleted'), default=False, db_index=True)

    objects = models.Manager.from_queryset(ValidKindsQuerySet)()

    @property
    def slug(self):
        return slugify(self.name)

    @property
    def cls_name(self):
        return Kind.CLS.text_of(self.cls)

    @staticmethod
    def cls_slug(cls):
        return slugify(str(Kind.CLS.text_of(cls)))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('kind')
        verbose_name_plural = _('kinds')
        ordering = 'cls', 'name'


class ValidFruitQuerySet(models.QuerySet):
    def valid(self):
        return self.exclude(models.Q(deleted=True) | models.Q(kind__deleted=True) | models.Q(user__is_active=False))


class Fruit(TimeStampedModel, GalleryModel):
    position = PointField(_('position'), null=True, blank=True, srid=4326)
    kind = models.ForeignKey(
        Kind, verbose_name=_('kind'),
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
        help_text=_('Please, provide as many information about the marker '
                    'as you find relevant.')
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

    objects = GalleryManager.from_queryset(ValidFruitQuerySet)()

    @property
    def is_deleted(self):
        return self.deleted or self.kind.deleted

    @property
    def reason_of_deletion(self):
        if self.kind.deleted:
            return _('Kind {kind} has been deleted.').format(kind=self.kind.name)

        if self.deleted:
            return self.why_deleted

        return ''

    def is_owner(self, user):
        return self.user.is_active and (self.user == user)

    def get_absolute_url(self):
        return reverse('fruit:detail', args=[self.id])

    def __str__(self):
        return '{fruit.kind!s}'.format(fruit=self)

    class Meta:
        verbose_name = _('fruit')
        verbose_name_plural = _('fruit')
