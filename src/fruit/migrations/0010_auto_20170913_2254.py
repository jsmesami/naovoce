# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fruit', '0009_copy-position'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fruit',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='fruit',
            name='longitude',
        ),
    ]
