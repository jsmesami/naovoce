from rest_framework import generics

from . import serializers
from ..models import FruitUser
from ..views import fruit_counter


class UserList(generics.ListAPIView):
    queryset = FruitUser.objects.iterator()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = FruitUser.objects.annotate(**fruit_counter)
    serializer_class = serializers.VerboseUserSerializer
