# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fruit', '0005_fruit_catalogue'),
    ]

    operations = [
        migrations.AddField(
            model_name='herbarium',
            name='new_url',
            field=models.URLField(verbose_name='url to new herbarium', blank=True),
        ),
    ]
