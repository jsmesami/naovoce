# Generated by Django 2.2.24 on 2021-07-18 18:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_facebookinfo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='read',
            new_name='is_read',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='system',
            new_name='is_system',
        ),
    ]
