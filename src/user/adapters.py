from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from rest_framework.reverse import reverse

from user.models import FruitUser


class AccountAdapter(DefaultAccountAdapter):
    """
    Allauth account adapter that does not use 'django.contrib.messages' if used by API.
    """
    def add_message(self, request, *args, **kwargs):
        if not request.path.startswith(reverse('api:root')):
            super().add_message(request, *args, **kwargs)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Allauth account adapter that automatically connects social accounts to existing accounts.
    """
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
            user = FruitUser.objects.get(email__iexact=email)
        except (FruitUser.DoesNotExist, KeyError):
            return

        sociallogin.connect(request, user)
