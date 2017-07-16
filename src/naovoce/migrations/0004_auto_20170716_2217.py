# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('naovoce', '0003_auto_20161108_1627'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Media',
        ),
        migrations.DeleteModel(
            name='Upload',
        ),
    ]
