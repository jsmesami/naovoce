from django.utils.translation import ugettext_lazy as _
from rest_framework import relations, serializers
from rest_framework.exceptions import ValidationError
from rest_framework.reverse import reverse

from fruit.models import Kind


class KindRelatedField(relations.RelatedField):

    queryset = Kind.objects.valid()

    def to_representation(self, value):
        return value.key

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(key=data)
        except Kind.DoesNotExist:
            raise ValidationError(_("{} is not a valid Kind key.").format(data))


class HyperlinkedFruitField(serializers.HyperlinkedIdentityField):
    def __init__(self, filter, **kwargs):  # noqa:A002
        self.filter = filter
        super().__init__("api:fruit-list", **kwargs)

    def get_url(self, obj, view_name, request, format):  # noqa:A002
        return "{url}?{filter}={value}".format(
            url=reverse(view_name, request=request, format=format),
            filter=self.filter,
            value=obj.id,
        )
