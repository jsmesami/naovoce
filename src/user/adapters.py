import smtplib
import logging

from allauth.account.models import EmailAddress
from allauth.account.utils import user_email, setup_user_email
from allauth.account.adapter import get_adapter as get_account_adapter
import allauth.socialaccount.models
from django.core.mail import mail_managers
from django.utils.translation import ugettext
from django.contrib import messages

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from rest_framework.reverse import reverse

from user.models import FruitUser


logger = logging.getLogger(__name__)


class AccountAdapter(DefaultAccountAdapter):

    def send_confirmation_mail(self, request, emailconfirmation, signup):
        """
        Do not just fail for typo in recipient email.
        """
        try:
            super().send_confirmation_mail(request, emailconfirmation, signup)
        except smtplib.SMTPRecipientsRefused as e:
            error_msg = ugettext(
                'Confirmation email has NOT been sent to {} (recipient refused).'
            ).format(emailconfirmation.email_address.email)
            logger.error(error_msg)
            self.add_message(
                request,
                messages.constants.ERROR,
                error_msg + ugettext('\nAdministrators have been notified.'),
            )
            mail_managers(error_msg, str(e))

    def add_message(self, request, *args, **kwargs):
        """
        Do not use 'django.contrib.messages' if used by API.
        """
        if not request.path.startswith(reverse('api:root')):
            super().add_message(request, *args, **kwargs)


def save_signup(self, request, connect=False):
    if self.is_existing:
        return

    user = self.user
    user.save()

    self.account.user = user
    self.account.save()

    self.token.account = self.account
    self.token.save()

    if not connect:
        setup_user_email(request, user, self.email_addresses)


# Monkeypatch stupid fucking Allauth
allauth.socialaccount.models.SocialLogin.save = save_signup


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Allauth account adapter that automatically connects social accounts to existing accounts.
    """
    existing_user = None

    def pre_social_login(self, request, sociallogin):
        """
        It there is an existing user, connect him to an account with the same email.
        """
        # If social account exists, just proceed.
        if sociallogin.is_existing:
            return

        # Connect social account if there is existing Django user with the same email.
        try:
            email = sociallogin.account.extra_data['email'].lower()
            self.existing_user = FruitUser.objects.get(email__iexact=email)
        except (FruitUser.DoesNotExist, KeyError):
            return

        sociallogin.connect(request, self.existing_user)

    def save_user(self, request, sociallogin, form=None):
        user = sociallogin.user

        if not self.existing_user:
            user.set_unusable_password()
            get_account_adapter().populate_username(request, user)

        sociallogin.save(request)

        return user

    def is_auto_signup_allowed(self, request, sociallogin):
        return bool(user_email(sociallogin.user))
