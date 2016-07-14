# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('amount', models.DecimalField(max_digits=10, decimal_places=2)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PayPalResponse',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('payment_id', models.CharField(null=True, blank=True, max_length=256, db_index=True)),
                ('currencycode', models.CharField(null=True, blank=True, max_length=32)),
                ('amount', models.DecimalField(max_digits=7, null=True, blank=True, decimal_places=2)),
                ('status', models.CharField(null=True, blank=True, max_length=256)),
                ('raw_response', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('donation', models.ForeignKey(to='donate.Donation', null=True)),
            ],
            options={
                'verbose_name_plural': 'PayPal Responses',
                'verbose_name': 'PayPal Response',
            },
        ),
    ]
