from rest_framework import serializers
from rest_framework import fields

from ..models import Herbarium


class HerbariumSerializer(serializers.ModelSerializer):

    name = fields.ReadOnlyField(
        source='kind.__str__',
    )

    kind_key = fields.ReadOnlyField(
        source='kind.key',
    )

    class Meta:
        model = Herbarium
        fields = 'name latin_name description photo kind_key'.split()
