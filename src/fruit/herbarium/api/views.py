from rest_framework import generics

from . import serializers
from ..models import Herbarium


class HerbariumList(generics.ListAPIView):
    """
    List Herbarium resources.
    """
    queryset = Herbarium.objects.select_related('kind').order_by()
    serializer_class = serializers.HerbariumSerializer
