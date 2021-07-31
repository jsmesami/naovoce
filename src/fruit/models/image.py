import logging
import os
from uuid import uuid4

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from utils.models import TimeStampedModel

logger = logging.getLogger(__name__)


class Image(TimeStampedModel):
    def _upload_to(self, filename):
        mangled_name = uuid4().hex + os.path.splitext(filename)[1]

        return f"fruit/{self.fruit_id}/images/{mangled_name}"

    image = models.ImageField(_("image"), upload_to=_upload_to)

    caption = models.CharField(_("caption"), max_length=280, blank=True)

    fruit = models.ForeignKey("fruit.Fruit", related_name="images", on_delete=models.CASCADE)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("author"),
        related_name="images",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    def is_owner(self, user):
        """For permissions to modify image"""
        return self.author == user

    def __str__(self):
        filename, ext = os.path.splitext(os.path.basename(self.image.path))
        return filename + ext if len(filename) < 19 else "...{}".format(filename[-16:] + ext)

    class Meta:
        ordering = ("-created",)
        verbose_name = _("image")
        verbose_name_plural = _("images")

    @classmethod
    def post_create(cls, sender, instance, created, *args, **kwargs):
        if created:
            logger.info(
                "Image for fruit {fruit_id} created by user {user!s} ({is_fruit_owner} fruit owner).".format(
                    fruit_id=instance.fruit_id,
                    user=instance.author,
                    is_fruit_owner="IS" if instance.author == instance.fruit.user else "NOT",
                )
            )


post_save.connect(Image.post_create, sender=Image)
