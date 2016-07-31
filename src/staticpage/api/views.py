from django.core.urlresolvers import reverse
from rest_framework.generics import ListAPIView

from .settings import ALLOWED_URLPATTERS
from . import serializers
from ..models import StaticPage


def get_allowed_urls():
    return (reverse(name) for name in ALLOWED_URLPATTERS)


class PagesList(ListAPIView):
    def get_serializer_class(self):
        raw = self.request.query_params.get('raw') is not None
        return serializers.PageRawSerializer if raw else serializers.PageSerializer

    def get_queryset(self):
        return StaticPage.objects.filter(url__in=get_allowed_urls())
