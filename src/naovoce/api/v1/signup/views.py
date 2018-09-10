from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers


class UserSignup(APIView):
    serializer_class = serializers.SignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save(self.request)

        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
        })


class UserSignupFacebook(APIView):
    serializer_class = serializers.SignupFacebookSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save(self.request)

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'id': user.id,
        })
