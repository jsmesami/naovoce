# Generated by Django 2.0.8 on 2018-09-16 12:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('herbarium', '0001_initial'),
        ('fruit', '0017_auto_20180916_1442'),
    ]

    operations = [
        migrations.RunSQL('INSERT INTO herbarium_herbarium'
                          '(id, full_name, full_name_cs, full_name_en, latin_name, description, photo, kind_id)'
                          'SELECT id, full_name, full_name_cs, full_name_en, latin_name, description, photo, kind_id '
                          'FROM fruit_herbarium'),
        migrations.RunSQL('INSERT INTO herbarium_season'
                          '(id, part, part_cs, part_en, start, duration, herb_id)'
                          'SELECT id, part, part_cs, part_en, start, duration, herb_id '
                          'FROM fruit_season'),
    ]