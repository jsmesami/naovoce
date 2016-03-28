# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import utils.fields
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_added_indexes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fruituser',
            name='avatar',
            field=utils.fields.ContentTypeRestrictedImageField(blank=True, verbose_name='avatar', help_text='User avatar', upload_to=user.models.FruitUser._upload_avatar_to, null=True),
        ),
    ]
