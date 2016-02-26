from rest_framework import generics
from rest_framework.response import Response


from . import serializers
from ..models import FruitUser
from ..views import fruit_counter


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


class UserDetail(generics.RetrieveAPIView):
    """
    Retreive specific User resource.
    """
    queryset = FruitUser.objects.annotate(**fruit_counter())
    serializer_class = serializers.VerboseUserSerializer
