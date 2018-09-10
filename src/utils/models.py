from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .fields import AutoDateTimeField


class TimeStampedModel(models.Model):
    """An abstract base class model that provides self-managed timezone-aware "created" and "modified" fields."""

    created = models.DateTimeField(_('created'), default=timezone.now, editable=False, db_index=True)
    modified = AutoDateTimeField(_('modified'), default=timezone.now, editable=False)

    class Meta:
        abstract = True
