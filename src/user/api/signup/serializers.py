from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import ugettext_lazy as _

from requests.exceptions import HTTPError

from rest_framework import serializers
from rest_framework import exceptions

from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import get_adapter as get_account_adapter
from allauth.socialaccount.adapter import get_adapter as get_socialaccount_adapter
from allauth.account.utils import setup_user_email, complete_signup
from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.models import SocialAccount, SocialLogin, SocialToken, SocialApp
from allauth.socialaccount.providers.facebook.views import fb_complete_login
from allauth.utils import email_address_exists, get_username_max_length


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=get_username_max_length(),
        min_length=allauth_settings.USERNAME_MIN_LENGTH,
        required=allauth_settings.USERNAME_REQUIRED
    )
    email = serializers.EmailField(
        required=allauth_settings.EMAIL_REQUIRED,
        style={'input_type': 'email'},
    )
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate_username(self, username):
        try:
            return get_account_adapter().clean_username(username)
        except DjangoValidationError:
            raise serializers.ValidationError(
                _("A user is already registered with this username."))

    def validate_email(self, email):
        email = get_account_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def validate_password(self, password):
        return get_account_adapter().clean_password(password)

    def validate(self, attrs):
        attrs['password1'] = attrs['password']  # Needed by save_user()
        return attrs

    def save(self, request):
        self.cleaned_data = self.validated_data  # Needed by new_user()
        user = get_account_adapter().new_user(request)
        original_request = request._request

        get_account_adapter().save_user(request, user, self)
        setup_user_email(request, user, [])
        complete_signup(original_request, user, allauth_settings.EMAIL_VERIFICATION, None)

        return user


class SignupFacebookSerializer(serializers.Serializer):
    email = serializers.CharField(style={'input_type': 'email'})
    fcb_id = serializers.CharField(style={'input_type': 'password'})
    fcb_token = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        try:
            account = SocialAccount.objects.get(user__email__iexact=attrs.get('email'))
        except SocialAccount.DoesNotExist:
            attrs['user'] = None
        else:
            if account.uid != attrs.get('fcb_id'):
                msg = _('Facebook ID does not match.')
                raise serializers.ValidationError(msg)

            if not account.user.is_active:
                raise serializers.ValidationError(
                    _('User account is disabled.')
                )

            attrs['user'] = account.user

        return attrs

    def save(self, request):
        user = self.validated_data['user']

        if user:
            return user
        else:
            app = SocialApp.objects.get(provider='facebook')
            social_token = SocialToken(app=app, token=self.validated_data['fcb_token'])

            try:
                # Check token against Facebook
                original_request = request._request
                login = fb_complete_login(original_request, app, social_token)
                login.token = social_token
                login.state = SocialLogin.state_from_request(original_request)
                complete_social_login(original_request, login)
            except HTTPError:
                # 400 Client Error
                raise exceptions.AuthenticationFailed(
                    _('Facebook authentication failed.')
                )
            else:
                self.cleaned_data = self.validated_data  # Needed by save_user()
                return get_socialaccount_adapter().save_user(request, login, self)
