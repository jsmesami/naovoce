# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_message'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fruituser',
            options={'ordering': ('-date_joined',), 'verbose_name_plural': 'users', 'verbose_name': 'user'},
        ),
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ('-created',), 'verbose_name_plural': 'messages', 'verbose_name': 'message'},
        ),
        migrations.AlterField(
            model_name='message',
            name='read',
            field=models.BooleanField(help_text='user.Message', verbose_name='user.Message', default=False),
        ),
        migrations.AlterField(
            model_name='message',
            name='recipient',
            field=models.ForeignKey(verbose_name='recipient', related_name='messages', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='message',
            name='system',
            field=models.BooleanField(help_text='System messages can be translated and can contain HTML.', verbose_name='user.Message', default=False),
        ),
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.CharField(max_length=255, verbose_name='text'),
        ),
    ]
