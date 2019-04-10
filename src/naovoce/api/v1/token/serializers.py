from django.utils.translation import ugettext_lazy as _
from facebook import GraphAPIError
from rest_framework import serializers
from user import constants
from user.models import FruitUser

from ..utils import facebook as fcb


class AuthTokenFacebookSerializer(serializers.Serializer):

    email = serializers.EmailField(
        required=True,
        allow_null=False,
        max_length=constants.EMAIL_MAX_LENGTH,
    )

    fcb_id = serializers.CharField(
        required=True,
        allow_null=False,
        max_length=constants.FCB_ID_MAX_LENGTH,
    )

    default_error_messages = {
        'facebook_verification': _('Facebook verification failed: {context}'),
        'user_does_not_exist': _('User with email {email} and Facebook ID {fcb_id} does not exist.'),
        'user_disabled': _('User account with email {email} is disabled.'),
    }

    def validate(self, attrs):
        email = attrs.get('email')
        fcb_id = attrs.get('fcb_id')

        try:
            user = FruitUser.objects.get(email__iexact=email, facebook__fcb_id=fcb_id)
        except FruitUser.DoesNotExist:
            self.fail('user_does_not_exist', email=email, fcb_id=fcb_id)

        if not user.is_active:
            self.fail('user_disabled', email=email)

        fcb_info = user.facebook

        try:
            fcb_user = fcb.verify_user(fcb_info.fcb_id, fcb_info.fcb_token)
        except GraphAPIError as e:
            self.fail('facebook_verification', context=e)

        return {
            'user': user,
            'fcb_user': fcb_user,
            'fcb_token': fcb_info.fcb_token,
            **attrs
        }

    def save(self, **kwargs):
        fcb_user = self.validated_data['fcb_user']
        user = self.validated_data['user']
        fcb_id = self.validated_data['fcb_id']
        fcb_token = self.validated_data['fcb_token']

        return fcb.connect_user(fcb_user, user, fcb_id, fcb_token),
