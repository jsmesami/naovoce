from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from facebook import GraphAPIError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from user import constants
from user.models import FruitUser

from ..utils import facebook as fcb


class SignupSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        max_length=constants.USERNAME_MAX_LENGTH,
        validators=[
            UniqueValidator(
                queryset=FruitUser.objects.all(),
                message=_('User with this username already exists.'),
            ),
        ],
    )
    email = serializers.EmailField(
        max_length=constants.EMAIL_MAX_LENGTH,
        validators=[
            UniqueValidator(
                queryset=FruitUser.objects.all(),
                message=_('User with this email already exists.')
            ),
        ],
    )
    password = serializers.CharField(
        write_only=True,
        min_length=settings.PASSWORD_MIN_LENGTH,
        max_length=constants.PASSWORD_MAX_LENGTH,
    )

    def create(self, validated_data):
        user = FruitUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user

    class Meta:
        model = FruitUser
        fields = 'id username email password'.split()


class SignupFacebookSerializer(serializers.Serializer):

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
    fcb_token = serializers.CharField(
        required=True,
        allow_null=False,
        max_length=constants.FCB_TOKEN_MAX_LENGTH,
    )

    default_error_messages = {
        'facebook_verification': _('Facebook verification failed: {context}'),
    }

    def validate(self, attrs):
        fcb_id = attrs.get('fcb_id')
        fcb_token = attrs.get('fcb_token')

        try:
            fcb_user = fcb.verify_user(fcb_id, fcb_token)
        except GraphAPIError as e:
            self.fail('facebook_verification', context=e)

        return {
            'fcb_user': fcb_user,
            **attrs
        }

    def save(self, **kwargs):
        email = self.validated_data['email']
        fcb_user = self.validated_data['fcb_user']
        fcb_id = self.validated_data['fcb_id']
        fcb_token = self.validated_data['fcb_token']

        try:
            user = FruitUser.objects.get(email__iexact=email)
        except FruitUser.DoesNotExist:
            user = fcb.create_user(fcb_user, email, fcb_id, fcb_token)
        else:
            user = fcb.connect_user(fcb_user, user, fcb_id, fcb_token)

        return user
