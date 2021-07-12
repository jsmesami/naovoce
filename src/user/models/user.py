import hashlib
import os
import urllib.parse
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail import get_thumbnail

import newsletter.list as newsletter
from utils.choices import Choices
from utils.full_url import get_full_url

from .. import constants
from .message import Message

AVATARS = {
    "SIZE": 240,
    "DEFAULT_AVATAR_URL": os.path.join(settings.STATIC_URL, "avatar.png"),
    "PATH_PREFIX": "avatars",
    **getattr(settings, "AVATARS", {}),
}


class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        """Create and save a User with the given username, email and password."""

        if not username:
            raise ValueError("A username must be set")

        if not email:
            raise ValueError("Users must have an email address")

        now = timezone.now()
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
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
    username = models.CharField(_("username"), max_length=constants.USERNAME_MAX_LENGTH, unique=True)
    email = models.EmailField(_("email address"), max_length=constants.EMAIL_MAX_LENGTH, unique=True)

    first_name = models.CharField(_("first name"), max_length=constants.FIRST_NAME_MAX_LENGTH, blank=True)
    last_name = models.CharField(_("last name"), max_length=constants.LAST_NAME_MAX_LENGTH, blank=True)
    external_url = models.URLField(_("external URL"), blank=True)

    RESOLUTION = Choices(
        picker=(1000, _("picker")),
        source=(2000, _("external source")),
    )
    resolution = models.IntegerField(
        _("resolution"),
        choices=RESOLUTION.choices,
        default=RESOLUTION.picker,
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can sign into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. " "Unselect this instead of deleting accounts."
        ),
    )
    is_email_verified = models.BooleanField(_("verified"), default=False)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    motto = models.CharField(_("motto"), max_length=255, blank=True)

    def _upload_avatar_to(self, filename):
        mangled_name = uuid4().hex[:8] + os.path.splitext(filename)[1]

        return "{base}/{id}/{file}".format(
            base=AVATARS["PATH_PREFIX"],
            id=self.id,
            file=mangled_name,
        )

    avatar = models.ImageField(
        _("avatar"),
        upload_to=_upload_avatar_to,
        blank=True,
        null=True,
        help_text=_("User avatar"),
    )

    objects = UserManager.from_queryset(ActiveUserQuerySet)()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ("email",)

    def get_full_name(self):
        return " ".join((self.first_name, self.last_name)).strip() or self.username

    def get_short_name(self):
        return self.username

    def get_avatar(self, request):
        size = AVATARS["SIZE"]

        if self.avatar:
            try:
                img = get_thumbnail(
                    self.avatar.file,
                    "{}x{}".format(size, size),
                    crop="center",
                    quality=90,
                )
            except FileNotFoundError:
                pass
            else:
                return get_full_url(request, img.url)

        fallback = get_full_url(
            request,
            (self.facebook_info and self.facebook_info.picture_url) or AVATARS["DEFAULT_AVATAR_URL"],
        )

        return "https://secure.gravatar.com/avatar/{hash}?{params}".format(
            hash=self.hash,
            params=urllib.parse.urlencode(dict(d=fallback, s=str(size))),
        )

    @property
    def facebook_info(self):
        try:
            return self.facebook
        except ObjectDoesNotExist:
            return None

    def has_newsletter(self):
        mailing_list = newsletter.List.get_default()
        return mailing_list.is_subscribed(self) if mailing_list else False

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
    def hash(self):  # noqa:A003
        return hashlib.md5(self.email.lower().encode("ascii", "ignore")).hexdigest()

    def __str__(self):
        return "{}".format(self.username)

    class Meta:
        ordering = ("-date_joined",)
        verbose_name = _("user")
        verbose_name_plural = _("users")
