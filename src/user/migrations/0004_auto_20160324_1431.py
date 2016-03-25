# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='fruituser',
            name='avatar',
            field=sorl.thumbnail.fields.ImageField(help_text='User icon', blank=True, null=True, verbose_name='avatar', upload_to='avatars'),
        ),
        migrations.AddField(
            model_name='fruituser',
            name='motto',
            field=models.CharField(verbose_name='motto', max_length=255, blank=True),
        ),
    ]
