from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from . import serializers


class UserSignupFacebook(APIView):
    serializer_class = serializers.SignupFacebookSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context=dict(request=request))
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        token, reated = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'id': user.id,
        })
