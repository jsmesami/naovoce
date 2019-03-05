# Generated by Django 2.2 on 2019-04-04 10:05

from django.conf import settings
import django.contrib.postgres.fields.hstore
from django.db import migrations, models
import django.utils.timezone
import utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_auto_20190222_1352'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacebookInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', utils.fields.AutoDateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('fcb_id', models.CharField(db_index=True, max_length=200, verbose_name='facebook ID')),
                ('fcb_token', models.CharField(max_length=500, verbose_name='access token')),
                ('picture_url', models.CharField(blank=True, max_length=500, verbose_name='URL to facebook avatar')),
                ('raw_data', django.contrib.postgres.fields.hstore.HStoreField(blank=True, null=True, verbose_name='raw data')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='facebook', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'facebook info',
                'verbose_name': 'facebook info',
            },
        ),
    ]
