from django.utils.translation import ugettext_lazy as _

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from .serializers import AuthTokenFacebookSerializer


class GetAuthToken(ObtainAuthToken):
    """
    Extends ObtainAuthToken to provide user ID in a response.
    """
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        if not user.is_email_verified:
            raise PermissionDenied(_("User's email is not verified."))

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'id': user.id,
        })


class GetAuthTokenFacebook(GetAuthToken):
    """
    Returns Auth token for user email and Facebook ID.
    """
    serializer_class = AuthTokenFacebookSerializer
