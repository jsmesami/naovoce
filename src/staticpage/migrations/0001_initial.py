# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StaticPage',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('url', models.CharField(max_length=50, unique=True, verbose_name='URL')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('text', models.TextField(blank=True, verbose_name='text')),
                ('meta_description', models.CharField(max_length=150, blank=True, verbose_name='meta description')),
            ],
            options={
                'verbose_name': 'static page',
                'verbose_name_plural': 'static pages',
            },
        ),
    ]
