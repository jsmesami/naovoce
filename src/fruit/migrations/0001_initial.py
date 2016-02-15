# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone
import utils.fields
import fruit.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Fruit',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', utils.fields.AutoDateTimeField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
                ('latitude', models.DecimalField(decimal_places=10, verbose_name='latitude', max_digits=13)),
                ('longitude', models.DecimalField(decimal_places=10, verbose_name='longitude', max_digits=13)),
                ('description', models.TextField(verbose_name='description', help_text='Please, provide as many information about the marker as you find relevant.', blank=True)),
                ('deleted', models.BooleanField(default=False, verbose_name='deleted')),
                ('why_deleted', models.TextField(verbose_name='why deleted', help_text='The tree has been cut down, not found etc.', blank=True)),
            ],
            options={
                'verbose_name_plural': 'fruit',
                'verbose_name': 'fruit',
            },
        ),
        migrations.CreateModel(
            name='Herbarium',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, verbose_name='full name', max_length=255)),
                ('full_name_en', models.CharField(null=True, blank=True, verbose_name='full name', max_length=255)),
                ('full_name_cs', models.CharField(null=True, blank=True, verbose_name='full name', max_length=255)),
                ('latin_name', models.CharField(blank=True, verbose_name='latin name', max_length=255)),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('photo', models.ImageField(null=True, upload_to='herbarium', blank=True, verbose_name='photo', help_text='Illustrational photo')),
            ],
            options={
                'verbose_name_plural': 'herbarium items',
                'verbose_name': 'herbarium item',
            },
        ),
        migrations.CreateModel(
            name='Kind',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('cls', models.IntegerField(verbose_name='class', choices=[(1000, 'Trees'), (2000, 'Bushes'), (3000, 'Herbs'), (4000, 'Nuts')])),
                ('name', models.CharField(unique=True, verbose_name='name', max_length=255)),
                ('name_en', models.CharField(null=True, unique=True, verbose_name='name', max_length=255)),
                ('name_cs', models.CharField(null=True, unique=True, verbose_name='name', max_length=255)),
                ('color', models.CharField(default='AAFF32', verbose_name='color', help_text='Hex color triplet for map.', max_length=6)),
                ('key', models.CharField(default=fruit.models._get_random_key, unique=True, verbose_name='key', help_text='ID for API and also index in the markers font', max_length=4)),
            ],
            options={
                'verbose_name_plural': 'kinds',
                'ordering': ('cls', 'name'),
                'verbose_name': 'kind',
            },
        ),
        migrations.AddField(
            model_name='herbarium',
            name='kind',
            field=models.OneToOneField(to='fruit.Kind', verbose_name='kind'),
        ),
        migrations.AddField(
            model_name='fruit',
            name='kind',
            field=models.ForeignKey(to='fruit.Kind', verbose_name='kind', related_name='fruits'),
        ),
        migrations.AddField(
            model_name='fruit',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='user', related_name='fruits'),
        ),
    ]
