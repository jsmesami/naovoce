from django.db import models


# TODO: Delete this after squashing migrations:
class Herbarium(models.Model):
    class Meta:
        db_table = 'fruit_herbarium'
        managed = False


class Season(models.Model):
    class Meta:
        db_table = 'fruit_season'
        managed = False
