from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'fruit': reverse('api:fruit-list', request=request, format=format),
        'herbarium': reverse('api:herbarium-list', request=request, format=format),
        'kinds': reverse('api:kinds-list', request=request, format=format),
        'users': reverse('api:users-list', request=request, format=format),
    })
