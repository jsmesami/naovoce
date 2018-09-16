from herbarium.models import Herbarium, Season
from rest_framework import fields, serializers

from ..fields import MarkdownField


class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = 'part start duration'.split()


class HerbariumRawSerializer(serializers.ModelSerializer):

    name = fields.ReadOnlyField(
        source='kind.__str__',
    )

    kind_key = fields.ReadOnlyField(
        source='kind.key',
    )

    seasons = SeasonSerializer(
        many=True,
    )

    class Meta:
        model = Herbarium
        fields = 'name latin_name description seasons photo kind_key'.split()


class HerbariumSerializer(HerbariumRawSerializer):
    description = MarkdownField()
