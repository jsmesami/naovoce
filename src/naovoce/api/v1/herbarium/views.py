from herbarium.models import Herbarium
from rest_framework import generics

from . import serializers


class HerbariumList(generics.ListAPIView):
    """List Herbarium resources."""

    queryset = Herbarium.objects.select_related('kind').order_by()

    def get_serializer_class(self):
        raw = self.request.query_params.get('raw') is not None
        return serializers.HerbariumRawSerializer if raw else serializers.HerbariumSerializer
