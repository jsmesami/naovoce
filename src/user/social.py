from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from user.models import FruitUser


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Override Allauth 's default behaviour, so that we can automatically connect
    social accounts to existing accounts.
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
        except FruitUser.DoesNotExist:
            return

        sociallogin.connect(request, user)
