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
