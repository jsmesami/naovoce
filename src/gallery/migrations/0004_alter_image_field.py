# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import utils.fields
import gallery.models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0003_added_indexes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=utils.fields.ContentTypeRestrictedImageField(upload_to=gallery.models.Image._upload_to, verbose_name='image'),
        ),
    ]
