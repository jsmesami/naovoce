# Generated by Django 2.2.28 on 2022-04-23 22:53

import django.contrib.gis.db.models.fields
import django.utils.timezone
from django.db import migrations, models

import fruit.models.image
import fruit.models.kind
import utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Comment",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "created",
                    models.DateTimeField(
                        db_index=True, default=django.utils.timezone.now, editable=False, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    utils.fields.AutoDateTimeField(
                        default=django.utils.timezone.now, editable=False, verbose_name="modified"
                    ),
                ),
                ("text", models.CharField(max_length=1600, verbose_name="comment")),
                ("ip", models.GenericIPAddressField(null=True, verbose_name="author's IP address")),
                ("is_complaint", models.BooleanField(default=False, verbose_name="complaint")),
                ("is_rejected", models.BooleanField(default=False, verbose_name="rejected")),
            ],
            options={
                "verbose_name": "comment",
                "verbose_name_plural": "comments",
                "ordering": ("-created",),
            },
        ),
        migrations.CreateModel(
            name="Fruit",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "created",
                    models.DateTimeField(
                        db_index=True, default=django.utils.timezone.now, editable=False, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    utils.fields.AutoDateTimeField(
                        default=django.utils.timezone.now, editable=False, verbose_name="modified"
                    ),
                ),
                (
                    "position",
                    django.contrib.gis.db.models.fields.PointField(
                        blank=True, null=True, srid=4326, verbose_name="position"
                    ),
                ),
                (
                    "catalogue",
                    models.IntegerField(
                        choices=[(1000, "naovoce"), (2000, "revival")], default=1000, verbose_name="resolution"
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Please, provide as many information about the marker as you find relevant.",
                        verbose_name="description",
                    ),
                ),
                ("deleted", models.BooleanField(db_index=True, default=False, verbose_name="deleted")),
                (
                    "why_deleted",
                    models.TextField(
                        blank=True, help_text="The tree has been cut down, not found etc.", verbose_name="why deleted"
                    ),
                ),
            ],
            options={
                "verbose_name": "fruit",
                "verbose_name_plural": "fruit",
            },
        ),
        migrations.CreateModel(
            name="Image",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "created",
                    models.DateTimeField(
                        db_index=True, default=django.utils.timezone.now, editable=False, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    utils.fields.AutoDateTimeField(
                        default=django.utils.timezone.now, editable=False, verbose_name="modified"
                    ),
                ),
                ("image", models.ImageField(upload_to=fruit.models.image.Image._upload_to, verbose_name="image")),
                ("caption", models.CharField(blank=True, max_length=280, verbose_name="caption")),
            ],
            options={
                "verbose_name": "image",
                "verbose_name_plural": "images",
                "ordering": ("-created",),
            },
        ),
        migrations.CreateModel(
            name="Kind",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "cls",
                    models.IntegerField(
                        choices=[(1000, "Trees"), (2000, "Bushes"), (3000, "Herbs"), (4000, "Nuts")],
                        verbose_name="class",
                    ),
                ),
                ("name", models.CharField(max_length=255, unique=True, verbose_name="name")),
                ("name_en", models.CharField(max_length=255, null=True, unique=True, verbose_name="name")),
                ("name_cs", models.CharField(max_length=255, null=True, unique=True, verbose_name="name")),
                (
                    "color",
                    models.CharField(
                        default="AAFF32", help_text="Hex color triplet for map.", max_length=6, verbose_name="color"
                    ),
                ),
                (
                    "key",
                    models.CharField(
                        default=fruit.models.kind._get_random_key,
                        help_text="ID for API and also index in the markers font",
                        max_length=4,
                        unique=True,
                        verbose_name="key",
                    ),
                ),
                ("deleted", models.BooleanField(db_index=True, default=False, verbose_name="deleted")),
            ],
            options={
                "verbose_name": "kind",
                "verbose_name_plural": "kinds",
                "ordering": ("cls", "name"),
            },
        ),
    ]
