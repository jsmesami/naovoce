import hashlib
import os
from uuid import uuid4

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.postgres.fields import HStoreField
from django.db import models
from django.utils import timezone
from django.utils.formats import date_format
from django.utils.functional import cached_property
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.utils.translation import ugettext, pgettext_lazy, ugettext_lazy as _

from utils.avatar import AVATAR_MAX_FILESIZE, AVATARS_URL
from utils.choices import Choices
from utils.fields import ContentTypeRestrictedImageField
from utils.models import TimeStampedModel

import newsletter.list as newsletter


class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('A username must be set')
        if not email:
            raise ValueError('Users must have an email address')

        now = timezone.now()
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, True, True, **extra_fields)


class ActiveUserQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True, is_email_verified=True)


class FruitUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=30, unique=True)
    email = models.EmailField(_('email address'), max_length=254, unique=True)

    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    external_url = models.URLField(_('external URL'), blank=True)

    RESOLUTION = Choices(
        picker=(1000, _('picker')),
        source=(2000, _('external source')),
    )
    resolution = models.IntegerField(
        _('resolution'),
        choices=RESOLUTION.choices,
        default=RESOLUTION.picker,
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can sign into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Designates whether this user should be treated as active. '
                    'Unselect this instead of deleting accounts.'),
    )
    is_email_verified = models.BooleanField(_('verified'), default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    motto = models.CharField(_('motto'), max_length=255, blank=True)

    def _upload_avatar_to(self, filename):
        return '{base}/custom/{id}/{file}'.format(
            base=AVATARS_URL,
            id=self.id,
            file=self._mangle_avatar_name(filename),
        )

    avatar = ContentTypeRestrictedImageField(
        _('avatar'),
        upload_to=_upload_avatar_to,
        blank=True,
        null=True,
        help_text=_("User avatar"),
        content_types=['image/png', 'image/jpeg', 'image/gif'],
        max_upload_size=AVATAR_MAX_FILESIZE
    )

    objects = UserManager.from_queryset(ActiveUserQuerySet)()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = 'email',

    def get_full_name(self):
        return ' '.join((self.first_name, self.last_name)).strip() or self.username

    def get_short_name(self):
        return self.username

    def has_newsletter(self):
        mailing_list = newsletter.List.get_default()
        return mailing_list.is_subscribed(self) if mailing_list else False

    @staticmethod
    def _mangle_avatar_name(filename):
        return uuid4().hex[:8] + os.path.splitext(filename)[1]

    def send_message(self, text, system=False, context=None):
        Message.objects.create(
            text=text,
            system=system,
            context=context,
            recipient=self,
        )

    def get_unread_messages(self):
        return self.messages.filter(read=False)

    def clear_messages(self):
        self.messages.filter(read=False).update(read=True)

    @cached_property
    def slug(self):
        return slugify(self.username)

    @cached_property
    def hash(self):
        return hashlib.md5(self.email.lower().encode('ascii', 'ignore')).hexdigest()

    def __str__(self):
        return '{}'.format(self.username)

    class Meta:
        ordering = '-date_joined',
        verbose_name = _('user')
        verbose_name_plural = _('users')


class Message(TimeStampedModel):
    """
    Represents simple database-stored messages for users.
    """
    text = models.CharField(_('text'), max_length=255)
    context = HStoreField(
        _('context'), blank=True, null=True,
        help_text=_('Translation context for system messages')
    )
    read = models.BooleanField(
        pgettext_lazy('user.Message', 'read'),
        help_text=pgettext_lazy('Has been read or not.', 'user.Message'),
        default=False,
    )
    system = models.BooleanField(
        pgettext_lazy('user.Message', 'system'),
        help_text=_('System messages can be translated and can contain HTML.'),
        default=False,
    )
    recipient = models.ForeignKey(
        FruitUser,
        verbose_name=_('recipient'),
        related_name='messages',
        on_delete=models.CASCADE,
    )

    @property
    def formatted_text(self):
        text = ugettext(self.text)
        if self.system:
            if self.context:
                try:
                    text = format_html(text, **self.context)
                except KeyError:
                    pass
            else:
                text = mark_safe(text)

        return format_html(
            '<span class="date">{date}</span> {text}',
            date=date_format(self.created, 'SHORT_DATE_FORMAT', use_l10n=True),
            text=text,
        )

    def __str__(self):
        return self.formatted_text

    class Meta:
        ordering = '-created',
        verbose_name = _('message')
        verbose_name_plural = _('messages')
