# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import utils.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('fruit', '0003_added_indexes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('part', models.CharField(verbose_name='ripening plant part', max_length=255)),
                ('part_en', models.CharField(null=True, verbose_name='ripening plant part', max_length=255)),
                ('part_cs', models.CharField(null=True, verbose_name='ripening plant part', max_length=255)),
                ('start', utils.fields.MonthsField(validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(1)], verbose_name='ripening start', default=1, help_text='Month when specified plant part ripening starts.')),
                ('duration', utils.fields.MonthsField(validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(1)], verbose_name='ripening duration', default=1, help_text='Duration of ripening in months.')),
                ('herb', models.ForeignKey(to='fruit.Herbarium', verbose_name='herbarium item', related_name='seasons', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name_plural': 'ripening seasons',
                'verbose_name': 'ripening season',
            },
        ),
        migrations.AlterUniqueTogether(
            name='season',
            unique_together=set([('part', 'herb')]),
        ),
    ]
