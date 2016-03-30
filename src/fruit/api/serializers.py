from django.core.urlresolvers import reverse

from rest_framework import serializers

from user.api.serializers import UserSerializer
from gallery.api.fields import HyperlinkedGalleryField
from .fields import KindRelatedField
from ..models import Fruit, Kind


class KindSerializer(serializers.ModelSerializer):

    col = serializers.CharField(source='color')
    cls = serializers.CharField(source='cls_name')

    class Meta:
        model = Kind
        fields = 'key', 'name', 'col', 'cls'


class VerboseFruitSerializer(serializers.HyperlinkedModelSerializer):
    PLACEHOLDER_ID = 0

    def __init__(self, *args, **kwargs):
        super(VerboseFruitSerializer, self).__init__(*args, **kwargs)
        # pre-load identity URL with placeholder ID
        self.identity_url_pattern = self.context['request'].build_absolute_uri(reverse('api:fruit-detail', args=(self.PLACEHOLDER_ID,)))

    lat = serializers.DecimalField(
        max_digits=13,
        decimal_places=10,
        source='latitude',
    )

    lng = serializers.DecimalField(
        max_digits=13,
        decimal_places=10,
        source='longitude',
    )

    kind = KindRelatedField()

    time = serializers.DateTimeField(
        source='modified',
        format='%Y-%m-%d %H:%M:%S',
        required=False,
        read_only=True,
    )

    # do not use HyperlinkedIdentityField because of slowness
    url = serializers.SerializerMethodField()

    user = UserSerializer(read_only=True)

    images_count = serializers.IntegerField(read_only=True)

    images = HyperlinkedGalleryField(gallery_ct='fruit')

    def get_url(self, obj):
        # replace placeholder ID with real object ID
        return self.identity_url_pattern.replace('/%d/' % self.PLACEHOLDER_ID, '/%d/' % obj.pk)

    class Meta:
        model = Fruit
        fields = 'id lat lng kind time url description user images_count images'.split()


class FruitSerializer(VerboseFruitSerializer):

    class Meta:
        model = VerboseFruitSerializer.Meta.model
        fields = 'id lat lng kind time url'.split()


class VerboseDeletedFruitSerializer(VerboseFruitSerializer):

    deleted = serializers.BooleanField(read_only=True)

    why_deleted = serializers.CharField(read_only=True)

    class Meta:
        model = VerboseFruitSerializer.Meta.model
        fields = 'id kind time deleted why_deleted url description user images'.split()


class DeletedFruitSerializer(VerboseFruitSerializer):

    class Meta:
        model = VerboseFruitSerializer.Meta.model
        fields = 'id kind time url'.split()
