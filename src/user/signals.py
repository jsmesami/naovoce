from allauth.account.signals import email_confirmed, user_signed_up
from allauth.socialaccount.signals import pre_social_login
from django.core.mail import mail_managers
from django.dispatch import receiver
from django.utils.translation import ugettext_noop
from newsletter.list import ClientError, List


@receiver(email_confirmed)
def sync_email_verified(request, email_address, **kwargs):
    """Upon email verification, sync allauth's EmailAddress.verified with FruitUser.is_email_verified."""

    fruit_user = email_address.user
    if fruit_user.email == email_address.email:
        fruit_user.is_email_verified = True
        fruit_user.save()


@receiver(pre_social_login)
def sync_social_email_verified(request, sociallogin, **kwargs):
    # We always require email from new social account user,
    # and we naively assume that it is always verified.
    sociallogin.user.is_email_verified = True


@receiver(user_signed_up)
def user_signed_up_notification(request, user, **kwargs):
    """Notify managers that another user signed up."""

    from .models import FruitUser
    subject = 'User {} has just registered'.format(user.username)
    body = 'Users count: {}'.format(
        FruitUser.objects.filter(
            is_active=True,
            is_email_verified=True,
        ).count()
    )
    mail_managers(subject, body)


@receiver(email_confirmed)
def send_welcome_message(request, email_address, **kwargs):
    """Successful verification means user is logged in for the 1st time, send her a message."""

    msg_template = ugettext_noop(
        'Welcome! Before you start using this site, '
        'please take time to read our <a href="{url}">codex</a>.'
    )

    context = {'url': 'http://na-ovoce.cz/web/kodex'}

    email_address.user.send_message(msg_template, context=context, system=True)


@receiver(user_signed_up)
def newsletter_autosubscribe(request, user, **kwargs):
    try:
        List.get_default().subscribe(user)
    except ClientError:
        pass
