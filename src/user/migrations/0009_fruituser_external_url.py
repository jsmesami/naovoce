# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_add_user_resolution'),
    ]

    operations = [
        migrations.AddField(
            model_name='fruituser',
            name='external_url',
            field=models.URLField(verbose_name='external URL', blank=True),
        ),
    ]
