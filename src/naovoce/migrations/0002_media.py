# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('naovoce', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('date', models.DateField(verbose_name='date published')),
                ('logo', models.FileField(upload_to='partners/logos', verbose_name='logo')),
                ('type', models.IntegerField(default=1000, choices=[(1000, 'Online media'), (2000, 'Printed media'), (3000, 'TV / Radio')], verbose_name='type')),
                ('title', models.CharField(max_length=255, verbose_name='title', blank=True)),
                ('perex', models.TextField(verbose_name='perex', blank=True)),
                ('link', models.URLField(verbose_name='link', blank=True)),
            ],
            options={
                'verbose_name': 'partner',
                'ordering': ('-date',),
                'verbose_name_plural': 'partners',
            },
        ),
    ]
