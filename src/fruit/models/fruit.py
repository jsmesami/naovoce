import logging

from django.conf import settings
from django.contrib.gis.db.models import PointField
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from utils.choices import Choices
from utils.models import TimeStampedModel

logger = logging.getLogger(__name__)


class ValidFruitQuerySet(models.QuerySet):
    def valid(self):
        return self.exclude(models.Q(deleted=True) | models.Q(kind__deleted=True))


class Fruit(TimeStampedModel):
    position = PointField(_("position"), null=True, blank=True, srid=4326)
    kind = models.ForeignKey(
        "fruit.Kind",
        verbose_name=_("kind"),
        related_name="fruits",
        on_delete=models.CASCADE,
    )
    CATALOGUE = Choices(
        naovoce=(1000, "naovoce"),
        revival=(2000, _("revival")),
    )
    catalogue = models.IntegerField(
        _("resolution"),
        choices=CATALOGUE.choices,
        default=CATALOGUE.naovoce,
    )

    description = models.TextField(
        _("description"),
        blank=True,
        help_text=_("Please, provide as many information about the marker as you find relevant."),
    )
    deleted = models.BooleanField(_("deleted"), default=False, db_index=True)
    why_deleted = models.TextField(
        _("why deleted"),
        blank=True,
        help_text=_("The tree has been cut down, not found etc."),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("user"),
        related_name="fruits",
        on_delete=models.CASCADE,
    )

    objects = models.Manager.from_queryset(ValidFruitQuerySet)()

    @property
    def is_deleted(self):
        return self.deleted or self.kind.deleted

    @property
    def reason_of_deletion(self):
        if self.kind.deleted:
            return _("Kind {kind} has been deleted.").format(kind=self.kind.name)

        if self.deleted:
            return self.why_deleted

        return ""

    def is_owner(self, user):
        return self.user == user

    def get_absolute_url(self):
        return settings.FRONTEND_URLS.get("fruit-detail").format(id=self.id)

    def __str__(self):
        return f"{self.kind!s}"

    @classmethod
    def post_create(cls, sender, instance, created, *args, **kwargs):
        if created:
            logger.info(
                "Fruit {fruit_id} of kind {kind!s} created by user {user!s}.".format(
                    fruit_id=instance.id,
                    kind=instance.kind,
                    user=instance.user,
                )
            )

    class Meta:
        verbose_name = _("fruit")
        verbose_name_plural = _("fruit")


post_save.connect(Fruit.post_create, sender=Fruit)
