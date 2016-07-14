# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import utils.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', utils.fields.AutoDateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('file', models.FileField(upload_to='uploads', verbose_name='file')),
                ('title', models.CharField(help_text='You can assign a title for future reference.', blank=True, max_length=255, verbose_name='title')),
            ],
            options={
                'verbose_name_plural': 'uploads',
                'verbose_name': 'upload',
                'ordering': ('-created',),
            },
        ),
    ]
