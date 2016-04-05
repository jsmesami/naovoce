from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status

from django.utils.translation import ugettext_lazy as _


@api_view()
def api_root(request, format=None):
    return Response({
        'fruit': reverse('api:fruit-list', request=request, format=format),
        'herbarium': reverse('api:herbarium-list', request=request, format=format),
        'kinds': reverse('api:kinds-list', request=request, format=format),
        'users': reverse('api:users-list', request=request, format=format),
    })


@api_view()
def api_handler_404(request, format=None):
    return Response(
        data=dict(detail=_('Not found.')),
        status=status.HTTP_404_NOT_FOUND,
    )


class GetAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'id': user.id,
        })
