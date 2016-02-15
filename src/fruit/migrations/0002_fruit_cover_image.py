# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
        ('fruit', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fruit',
            name='cover_image',
            field=models.ForeignKey(blank=True, null=True, verbose_name='cover image', to='gallery.Image', on_delete=django.db.models.deletion.SET_NULL, related_name='+'),
        ),
    ]
