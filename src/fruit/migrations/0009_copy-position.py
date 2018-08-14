# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.gis.geos import Point
from django.db import migrations


def copy_position(apps, schema_editor):
    Fruit = apps.get_model("fruit", "Fruit")

    for fruit in Fruit.objects.all():
        fruit.position = Point(float(fruit.longitude), float(fruit.latitude))
        fruit.save()


def reverse(apps, schema_editor):
    Fruit = apps.get_model("fruit", "Fruit")

    for fruit in Fruit.objects.all():
        fruit.latitude = fruit.position.y
        fruit.longitude = fruit.position.x
        fruit.save()


class Migration(migrations.Migration):

    dependencies = [
        ('fruit', '0008_fruit_position'),
    ]

    operations = [
        migrations.RunPython(copy_position, reverse_code=reverse),
    ]
