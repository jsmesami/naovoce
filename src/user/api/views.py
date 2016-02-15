from rest_framework import generics
from django.db.models import Count, Case, When

from . import serializers
from ..models import FruitUser


class UserList(generics.ListAPIView):
    queryset = FruitUser.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = FruitUser.objects.annotate(
        fruit_count=Count(Case(When(fruits__deleted=False, then=1)))
    )
    serializer_class = serializers.VerboseUserSerializer
