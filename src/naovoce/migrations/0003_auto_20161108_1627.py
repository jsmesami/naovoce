# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('naovoce', '0002_media'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='media',
            options={'verbose_name': 'media', 'ordering': ('-date',), 'verbose_name_plural': 'media'},
        ),
    ]
