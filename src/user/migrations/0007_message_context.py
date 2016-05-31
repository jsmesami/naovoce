# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.contrib.postgres.fields.hstore import HStoreField
from django.contrib.postgres.operations import HStoreExtension


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_avatar_upload_to'),
    ]

    operations = [
        HStoreExtension(),
        migrations.AddField(
            model_name='message',
            name='context',
            field=HStoreField(verbose_name='context', help_text='Translation context for system messages', null=True, blank=True),
        ),
    ]
