# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('fruit', '0002_fruit_cover_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fruit',
            name='created',
            field=models.DateTimeField(verbose_name='created', db_index=True, editable=False, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='fruit',
            name='deleted',
            field=models.BooleanField(verbose_name='deleted', db_index=True, default=False),
        ),
    ]
