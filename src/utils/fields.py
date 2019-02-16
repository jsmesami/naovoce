from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class AutoDateTimeField(models.DateTimeField):
    """A field that saves timezone-aware datetime on each save."""

    def pre_save(self, model_instance, add):
        return timezone.now()


# TODO: Delete this after squashing migrations:
class ContentTypeRestrictedImageField(models.ImageField):
    pass


class MonthsField(models.PositiveSmallIntegerField):
    def __init__(self, *args, **kwargs):
        kwargs.update(dict(
            default=1,
            validators=[MaxValueValidator(12), MinValueValidator(1)],
            choices=zip(range(1, 13), range(1, 13)),
        ))
        super().__init__(*args, **kwargs)
