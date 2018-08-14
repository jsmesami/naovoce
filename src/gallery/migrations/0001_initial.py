# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import utils.fields
import sorl.thumbnail.fields
import gallery.models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', utils.fields.AutoDateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('image', sorl.thumbnail.fields.ImageField(upload_to=gallery.models.Image._upload_to, verbose_name='image')),
                ('caption', models.CharField(blank=True, max_length=140, verbose_name='caption')),
                ('gallery_id', models.PositiveIntegerField()),
                ('gallery_ct', models.ForeignKey(to='contenttypes.ContentType', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ('-created',),
                'verbose_name_plural': 'images',
                'verbose_name': 'image',
            },
        ),
    ]
