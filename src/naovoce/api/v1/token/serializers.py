from allauth.socialaccount.models import SocialAccount
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


class AuthTokenFacebookSerializer(serializers.Serializer):
    email = serializers.CharField(style={'input_type': 'email'})
    fcb_id = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        fcb_id = attrs.get('fcb_id')

        if email and fcb_id:
            try:
                account = SocialAccount.objects.get(user__email__iexact=email)
            except SocialAccount.DoesNotExist:
                msg = _('Facebook account does not exist.')
                raise serializers.ValidationError(msg)

            if account.uid != fcb_id:
                msg = _('Facebook ID does not match.')
                raise serializers.ValidationError(msg)

            if not account.user.is_active:
                msg = _('User account is disabled.')
                raise serializers.ValidationError(msg)

            attrs['user'] = account.user
        else:
            msg = _('Must include "username" and Facebook ID "fcb_id".')
            raise serializers.ValidationError(msg)

        return attrs
