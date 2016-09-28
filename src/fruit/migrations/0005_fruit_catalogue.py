# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fruit', '0004_add_seasons'),
    ]

    operations = [
        migrations.AddField(
            model_name='fruit',
            name='catalogue',
            field=models.IntegerField(default=1000, verbose_name='resolution', choices=[(1000, 'naovoce'), (2000, 'revival')]),
        ),
    ]
