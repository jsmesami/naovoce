# Generated by Django 2.2.28 on 2022-04-23 22:53

from django.conf import settings
import django.contrib.postgres.fields.hstore
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import user.models.user
import utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='FruitUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=30, unique=True, verbose_name='username')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('external_url', models.URLField(blank=True, verbose_name='external URL')),
                ('resolution', models.IntegerField(choices=[(1000, 'picker'), (2000, 'external source')], default=1000, verbose_name='resolution')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can sign into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('is_email_verified', models.BooleanField(default=False, verbose_name='verified')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('motto', models.CharField(blank=True, max_length=255, verbose_name='motto')),
                ('avatar', models.ImageField(blank=True, help_text='User avatar', null=True, upload_to=user.models.user.FruitUser._upload_avatar_to, verbose_name='avatar')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'ordering': ('-date_joined',),
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', utils.fields.AutoDateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('text', models.CharField(max_length=255, verbose_name='text')),
                ('context', django.contrib.postgres.fields.hstore.HStoreField(blank=True, help_text='Translation context for system messages', null=True, verbose_name='context')),
                ('is_read', models.BooleanField(default=False, help_text='user.Message', verbose_name='read')),
                ('is_system', models.BooleanField(default=False, help_text='System messages can be translated and can contain HTML.', verbose_name='system')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to=settings.AUTH_USER_MODEL, verbose_name='recipient')),
            ],
            options={
                'verbose_name': 'message',
                'verbose_name_plural': 'messages',
                'ordering': ('-created',),
            },
        ),
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
                'verbose_name': 'facebook info',
                'verbose_name_plural': 'facebook info',
            },
        ),
    ]
