from django.contrib.postgres.fields import HStoreField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.models import TimeStampedModel

from .. import constants


class FacebookInfo(TimeStampedModel):
    user = models.OneToOneField(
        "user.FruitUser",
        related_name="facebook",
        on_delete=models.CASCADE,
    )
    fcb_id = models.CharField(
        _("facebook ID"),
        db_index=True,
        max_length=constants.FCB_ID_MAX_LENGTH,
    )
    fcb_token = models.CharField(
        _("access token"),
        max_length=constants.FCB_TOKEN_MAX_LENGTH,
    )
    picture_url = models.CharField(
        _("URL to facebook avatar"),
        max_length=constants.FCB_PICTURE_URL_MAX_LENGTH,
        blank=True,
    )
    raw_data = HStoreField(
        _("raw data"),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("facebook info")
        verbose_name_plural = _("facebook info")
