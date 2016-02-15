from django.utils.translation import ugettext_lazy as _
from django.core.cache import caches
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS

from naovoce.api.permissions import IsOwnerOrReadOnly
from . import serializers
from ..models import Fruit, Kind


class CachedResponse(Response):

    cache = caches['fruit']

    def __init__(self, cache_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache_key = cache_key

    @property
    def rendered_content(self):
        # We cache json response only.
        # Note that self.content-type is not set yet.
        if self.accepted_media_type == 'application/json':
            content = self.cache.get(self.cache_key)
            if not content:
                content = super().rendered_content
                self.cache.set(self.cache_key, content)
        else:
            content = super().rendered_content

        return content

    @staticmethod
    @receiver(post_save, sender=Fruit)
    def on_fruit_save(*args, **kwargs):
        CachedResponse.cache.clear()

    @staticmethod
    @receiver(post_delete, sender=Fruit)
    def on_fruit_delete(*args, **kwargs):
        CachedResponse.cache.clear()


class FruitList(generics.ListCreateAPIView):
    queryset = Fruit.objects.valid().select_related('kind').order_by('-created')
    permission_classes = IsAuthenticatedOrReadOnly,

    def list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())

        user = request.query_params.get('user')
        if user:
            qs = qs.filter(user__id=int(user))

        kind = request.query_params.get('kind')
        if kind:
            qs = qs.filter(kind__key=kind)

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qs, many=True)

        if not user:
            # Caching comb. of both kind & user would produce too many cache entries.
            return CachedResponse(kind or 'all', serializer.data)
        else:
            return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return serializers.FruitSerializer

        return serializers.VerboseFruitSerializer

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
        )


class FruitDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Fruit.objects.select_related('kind', 'user')
    permission_classes = IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly

    def get_serializer_class(self):
        if self.get_object().deleted:
            return serializers.DeletedFruitSerializer

        return serializers.VerboseFruitSerializer

    def destroy(self, request, *args, **kwargs):
        # We never really delete Fruit, just set its status to deleted.
        instance = self.get_object()
        if instance.deleted:
            raise PermissionDenied(_('Cannot update once deleted object.'))

        instance.deleted = True
        instance.why_deleted = request.data.get('why_deleted', '')
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        # We cannot update fruit that has been deleted
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.deleted:
            raise PermissionDenied(_('Cannot update once deleted object.'))

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class KindList(generics.ListAPIView):
    queryset = Kind.objects.all()
    serializer_class = serializers.KindSerializer
