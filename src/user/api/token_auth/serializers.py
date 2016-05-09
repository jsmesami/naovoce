from django.utils.translation import ugettext_lazy as _
from allauth.socialaccount.models import SocialAccount
from rest_framework import serializers


class AuthTokenFacebookSerializer(serializers.Serializer):
    email = serializers.CharField(style={'input_type': 'email'})
    fcbid = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        fcbid = attrs.get('fcbid')

        if email and fcbid:
            try:
                account = SocialAccount.objects.get(user__email__iexact=email)
            except SocialAccount.DoesNotExist:
                msg = _('Facebook account does not exist.')
                raise serializers.ValidationError(msg)

            if account.uid != fcbid:
                msg = _('Facebook ID does not match.')
                raise serializers.ValidationError(msg)

            if not account.user.is_active:
                msg = _('User account is disabled.')
                raise serializers.ValidationError(msg)

            attrs['user'] = account.user
        else:
            msg = _('Must include "username" and Facebook ID "fcbid".')
            raise serializers.ValidationError(msg)

        return attrs
