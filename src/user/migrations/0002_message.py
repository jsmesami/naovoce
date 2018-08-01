# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import utils.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', utils.fields.AutoDateTimeField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
                ('text', models.CharField(verbose_name='Message', max_length=255)),
                ('read', models.BooleanField(help_text='Has been read or not.', default=False, verbose_name='Read')),
                ('system', models.BooleanField(help_text='Is it safe for escaping or not.', default=False, verbose_name='System')),
                ('recipient', models.ForeignKey(verbose_name='Message', related_name='messages', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'message',
                'verbose_name_plural': 'messages',
            },
        ),
    ]
