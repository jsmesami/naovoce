from rest_framework import serializers
from rest_framework import fields

from utils.api.fields import MarkdownField
from ..models import Herbarium


class HerbariumRawSerializer(serializers.ModelSerializer):

    name = fields.ReadOnlyField(
        source='kind.__str__',
    )

    kind_key = fields.ReadOnlyField(
        source='kind.key',
    )

    class Meta:
        model = Herbarium
        fields = 'name latin_name description photo kind_key'.split()


class HerbariumSerializer(HerbariumRawSerializer):
    description = MarkdownField()
