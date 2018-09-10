import logging
import smtplib
from user.models import FruitUser

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib import messages
from django.core.mail import mail_managers
from django.utils.translation import ugettext
from rest_framework.reverse import reverse

logger = logging.getLogger(__name__)


class AccountAdapter(DefaultAccountAdapter):

    def send_confirmation_mail(self, request, emailconfirmation, signup):
        """Do not just fail for typo in recipient email."""

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
        """Do not use 'django.contrib.messages' if used by API."""
        if not request.path.startswith(reverse('api:root')):
            super().add_message(request, *args, **kwargs)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    """Allauth account adapter that automatically connects social accounts to existing accounts."""

    def pre_social_login(self, request, sociallogin):
        """It there is an existing user, connect him to an account with the same email."""
        # If social account exists, just proceed.
        if sociallogin.is_existing:
            return

        # Connect social account if there is existing Django user with the same email.
        try:
            email = sociallogin.account.extra_data['email'].lower()
            user = FruitUser.objects.get(email__iexact=email)
        except (FruitUser.DoesNotExist, KeyError):
            return

        sociallogin.connect(request, user)
