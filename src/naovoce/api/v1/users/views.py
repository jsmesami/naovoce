import datetime

from rest_framework import generics
from rest_framework.response import Response

from user.models import FruitUser
from user.utils import fruit_counter, top_pickers
from . import serializers


class UserList(generics.ListAPIView):
    """
    List User resources.
    """
    queryset = FruitUser.objects.all()
    serializer_class = serializers.UserSerializer

    def list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # We are not paginating, so we can serialize iterator (saves memory)
        serializer = self.get_serializer(qs.iterator(), many=True)
        return Response(serializer.data)


class UserListTop(UserList):

    queryset = top_pickers()
    serializer_class = serializers.TopUserSerializer


class UserListTopLastMonth(UserList):

    serializer_class = serializers.TopUserSerializer

    def get_queryset(self):
        last_month = datetime.date.today() - datetime.timedelta(365 / 12)
        return top_pickers(fruits__created__gte=last_month).exclude(fruit_count=0)


class UserDetail(generics.RetrieveAPIView):
    """
    Retreive specific User resource.
    """
    queryset = FruitUser.objects.annotate(**fruit_counter())
    serializer_class = serializers.VerboseUserSerializer
