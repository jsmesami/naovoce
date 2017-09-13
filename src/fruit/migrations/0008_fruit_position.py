# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('fruit', '0007_migrate_herbarium_urls'),
    ]

    operations = [
        migrations.AddField(
            model_name='fruit',
            name='position',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, srid=4326, null=True, verbose_name='position'),
        ),
    ]
