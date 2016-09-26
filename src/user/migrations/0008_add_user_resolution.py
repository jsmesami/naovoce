# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_message_context'),
    ]

    operations = [
        migrations.AddField(
            model_name='fruituser',
            name='resolution',
            field=models.IntegerField(verbose_name='resolution', choices=[(1000, 'picker'), (2000, 'external source')], default=1000),
        ),
        migrations.AlterField(
            model_name='message',
            name='read',
            field=models.BooleanField(verbose_name='read', help_text='user.Message', default=False),
        ),
        migrations.AlterField(
            model_name='message',
            name='system',
            field=models.BooleanField(verbose_name='system', help_text='System messages can be translated and can contain HTML.', default=False),
        ),
    ]
