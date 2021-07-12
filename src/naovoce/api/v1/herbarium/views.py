from rest_framework import generics

from herbarium.models import Herbarium

from . import serializers


class HerbariumList(generics.ListAPIView):
    """List Herbarium resources."""

    queryset = Herbarium.objects.select_related("kind").prefetch_related("seasons")

    def get_serializer_class(self):
        raw = self.request.query_params.get("raw") is not None
        return serializers.HerbariumRawSerializer if raw else serializers.HerbariumSerializer
