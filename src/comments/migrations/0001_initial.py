# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import utils.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', utils.fields.AutoDateTimeField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
                ('text', models.CharField(verbose_name='comment', max_length=1600)),
                ('ip', models.GenericIPAddressField(null=True, verbose_name="author's IP address")),
                ('rejected', models.BooleanField(default=False, verbose_name='rejected')),
                ('object_id', models.PositiveIntegerField()),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name_plural': 'comments',
                'ordering': ('-created',),
                'verbose_name': 'comment',
            },
        ),
    ]
