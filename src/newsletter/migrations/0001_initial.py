# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import utils.fields
import newsletter.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('file', models.FileField(upload_to=newsletter.models.Asset._upload_to, verbose_name='file')),
            ],
            options={
                'verbose_name': 'asset',
                'verbose_name_plural': 'assets',
            },
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created', models.DateTimeField(verbose_name='created', editable=False, default=django.utils.timezone.now, db_index=True)),
                ('modified', utils.fields.AutoDateTimeField(verbose_name='modified', editable=False, default=django.utils.timezone.now)),
                ('subject', models.CharField(verbose_name='subject', max_length=255)),
                ('plain_text', models.TextField(verbose_name='plain text')),
                ('html_text', models.TextField(verbose_name='html text')),
                ('sent', models.BooleanField(verbose_name='sent', editable=False, default=False)),
                ('from_name', models.CharField(verbose_name='from name', max_length=255, default='Na ovoce newsletter')),
                ('from_email', models.EmailField(verbose_name='from email', max_length=255, default='newsletter@na-ovoce.cz')),
            ],
            options={
                'verbose_name': 'campaign',
                'verbose_name_plural': 'campaigns',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created', models.DateTimeField(verbose_name='created', editable=False, default=django.utils.timezone.now, db_index=True)),
                ('modified', utils.fields.AutoDateTimeField(verbose_name='modified', editable=False, default=django.utils.timezone.now)),
                ('name', models.CharField(verbose_name='name', max_length=255, unique=True)),
                ('hash', models.CharField(verbose_name='hash', max_length=255, unique=True)),
            ],
            options={
                'verbose_name': 'recipient list',
                'verbose_name_plural': 'recipient lists',
                'ordering': ('-created',),
            },
        ),
        migrations.AddField(
            model_name='campaign',
            name='lists',
            field=models.ManyToManyField(verbose_name='subscriber lists', related_name='campaigns', to='newsletter.List'),
        ),
        migrations.AddField(
            model_name='asset',
            name='campaign',
            field=models.ForeignKey(verbose_name='campaign', related_name='assets', to='newsletter.Campaign'),
        ),
    ]
