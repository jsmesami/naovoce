from rest_framework import serializers

from utils.avatar import get_avatar
from user.models import FruitUser
from ..fruit.fields import HyperlinkedFruitField


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FruitUser
        fields = 'id username url'.split()

        extra_kwargs = {
            'url': dict(view_name='api:users-detail')
        }


class AvatarField(serializers.HyperlinkedIdentityField):
    def __init__(self, **kwargs):
        super().__init__('', **kwargs)

    def get_url(self, obj, view_name, request, format):
        return get_avatar(request, obj)


class VerboseUserSerializer(UserSerializer):

    active = serializers.BooleanField(
        required=False,
        read_only=True,
        source='is_active',
    )

    fruit_count = serializers.IntegerField(read_only=True)

    fruit = HyperlinkedFruitField(filter='user')

    avatar = AvatarField()

    class Meta(UserSerializer.Meta):
        fields = 'id username url active fruit_count fruit avatar motto'.split()


class TopUserSerializer(UserSerializer):

    fruit_count = serializers.IntegerField(read_only=True)

    avatar = AvatarField()

    class Meta(UserSerializer.Meta):
        fields = 'id username url fruit_count avatar'.split()
