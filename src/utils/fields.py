from django.db import models
from django.utils import timezone


class AutoDateTimeField(models.DateTimeField):
    """
    A field that saves timezone-aware datetime on each save.
    """
    def pre_save(self, model_instance, add):
        return timezone.now()
