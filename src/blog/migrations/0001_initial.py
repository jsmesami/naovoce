# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import utils.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False, verbose_name='created', default=django.utils.timezone.now)),
                ('modified', utils.fields.AutoDateTimeField(editable=False, verbose_name='modified', default=django.utils.timezone.now)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('title_en', models.CharField(max_length=255, null=True, verbose_name='title')),
                ('title_cs', models.CharField(max_length=255, null=True, verbose_name='title')),
                ('text', models.TextField(verbose_name='text')),
                ('text_en', models.TextField(null=True, verbose_name='text')),
                ('text_cs', models.TextField(null=True, verbose_name='text')),
                ('public_from', models.DateTimeField(verbose_name='public from', default=django.utils.timezone.now)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False, verbose_name='author')),
            ],
            options={
                'verbose_name_plural': 'blog posts',
                'verbose_name': 'blog post',
                'ordering': ('-public_from', '-created'),
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name')),
                ('name_en', models.CharField(max_length=255, null=True, unique=True, verbose_name='name')),
                ('name_cs', models.CharField(max_length=255, null=True, unique=True, verbose_name='name')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.AddField(
            model_name='blogpost',
            name='categories',
            field=models.ManyToManyField(to='blog.Category', related_name='blogposts', verbose_name='categories'),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='cover_image',
            field=models.ForeignKey(null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, to='gallery.Image', blank=True, verbose_name='cover image'),
        ),
    ]
