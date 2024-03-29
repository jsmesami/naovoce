from django.contrib.gis.geos import Point
from rest_framework import serializers
from rest_framework.relations import HyperlinkedIdentityField

from fruit.models import Fruit, Kind

from ..fields import CachedHyperlinkedIdentityField
from ..users.serializers import UserSerializer
from .fields import KindRelatedField


class KindSerializer(serializers.ModelSerializer):

    col = serializers.CharField(source="color")

    cls = serializers.CharField(source="cls_name")

    class Meta:
        model = Kind
        fields = "key name col cls".split()


class VerboseFruitSerializer(serializers.HyperlinkedModelSerializer):

    lng = serializers.DecimalField(
        max_digits=13,
        decimal_places=10,
        source="position.x",
    )

    lat = serializers.DecimalField(
        max_digits=13,
        decimal_places=10,
        source="position.y",
    )

    kind = KindRelatedField()

    time = serializers.DateTimeField(
        source="modified",
        format="%Y-%m-%d %H:%M:%S",
        required=False,
        read_only=True,
    )

    # Used instead of HyperlinkedIdentityField because it's slow.
    url = CachedHyperlinkedIdentityField(view_name="api:fruit-detail")

    user = UserSerializer(read_only=True)

    images_count = serializers.IntegerField(read_only=True)

    images = HyperlinkedIdentityField(view_name="api:image-list", lookup_url_kwarg="fruit_pk")

    def create(self, validated_data):
        validated_data["position"] = Point(
            float(validated_data["position"]["x"]),
            float(validated_data["position"]["y"]),
        )

        return super().create(validated_data)

    def update(self, instance, validated_data):
        position = validated_data.pop("position")

        if "x" in position:
            instance.position.x = position["x"]

        if "y" in position:
            instance.position.y = position["y"]

        return super().update(instance, validated_data)

    class Meta:
        model = Fruit
        fields = "id lat lng kind time url description user images_count images".split()


class FruitSerializer(VerboseFruitSerializer):
    class Meta:
        model = VerboseFruitSerializer.Meta.model
        fields = "id lat lng kind time url".split()


class VerboseDeletedFruitSerializer(VerboseFruitSerializer):

    deleted = serializers.SerializerMethodField()

    why_deleted = serializers.SerializerMethodField()

    def get_deleted(self, obj):
        return obj.is_deleted

    def get_why_deleted(self, obj):
        return obj.reason_of_deletion

    class Meta:
        model = VerboseFruitSerializer.Meta.model
        fields = "id kind time deleted why_deleted url description user images".split()


class DeletedFruitSerializer(VerboseFruitSerializer):
    class Meta:
        model = VerboseFruitSerializer.Meta.model
        fields = "id kind time url".split()
