import hashlib

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.mail import mail_managers
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver

from allauth.account.signals import user_signed_up, email_confirmed


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


class FruitUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=30, unique=True)
    email = models.EmailField(_('email address'), max_length=254, unique=True)

    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
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

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = 'email',

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        return ' '.join((self.first_name, self.last_name)).strip() or self.username

    def get_short_name(self):
        return self.username

    def get_absolute_url(self):
        return reverse('pickers:detail', args=[self.pk, self.slug])

    @cached_property
    def slug(self):
        return slugify(self.username)

    @cached_property
    def hash(self):
        return hashlib.md5(self.email.lower().encode('ascii', 'ignore')).hexdigest()

    def __str__(self):
        return '{}'.format(self.username)


@receiver(email_confirmed)
def sync_email_verified(request, email_address, **kwargs):
    """
    Upon email verification, sync allauth's EmailAddress.verified
    with FruitUser.is_email_verified
    """
    fruit_user = email_address.user
    if fruit_user.email == email_address.email:
        fruit_user.is_email_verified = True
        fruit_user.save()


@receiver(user_signed_up)
def user_signed_up_notification(request, user, **kwargs):
    """
    Notify managers that another user signed up.
    """
    subject = 'User {} has just registered'.format(user.username)
    body = 'Users count: {}'.format(
        FruitUser.objects.filter(
            is_active=True,
            is_email_verified=True,
        ).count()
    )
    mail_managers(subject, body)
