from django.contrib.contenttypes.models import ContentType
from django.core.cache import caches
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.http.response import Http404
from django.utils.translation import ugettext_lazy as _
from fruit.models import Fruit, Kind
from ipware.ip import get_ip
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from . import serializers
from ..comments.serializers import CommentSerializer
from ..permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly


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
    """List or create Fruit resources."""

    queryset = Fruit.objects.valid().select_related('kind').order_by('-created')
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())

        catalogue = request.query_params.get('catalogue')
        if catalogue:
            qs = qs.filter(catalogue=int(catalogue))

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

        # We are not paginating, so we can serialize iterator (saves memory)
        serializer = self.get_serializer(qs.iterator(), many=True)

        if not (user or catalogue):
            # Caching comb. of both kind & user would produce too many cache entries.
            return CachedResponse(kind or 'all', serializer.data)

        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return serializers.FruitSerializer

        return serializers.VerboseFruitSerializer

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
        )


class FruitDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retreive, update or destroy specific Fruit resource."""

    queryset = Fruit.objects\
        .select_related('kind', 'user')\
        .annotate(images_count=Count('images'))
    permission_classes = IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly

    def get_serializer_class(self):
        if self.get_object().deleted:
            return serializers.VerboseDeletedFruitSerializer

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


class FruitComplaint(generics.CreateAPIView):
    """Use comment system to send a complaint on invalid Fruit marker."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        fruit = get_object_or_404(Fruit, pk=self.kwargs.get('pk'))

        serializer.save(
            author=self.request.user,
            ip=get_ip(self.request),
            complaint=True,
            content_type=ContentType.objects.get_for_model(fruit),
            object_id=fruit.id,
        )


class KindList(generics.ListAPIView):
    """List fruit Kinds resources."""

    queryset = Kind.objects.order_by()
    serializer_class = serializers.KindSerializer


@api_view()
def fruit_list_diff(request, date, time):
    """Get difference since date and/or time specified."""

    if not date:
        # The date is not mandatory in url regex, because otherwise we woudln't be able to
        # use URL template tag without knowing the date ahead (we get the date using JS).
        raise Http404

    since = ' '.join([date, time or '00:00:00'])

    fruit = Fruit.objects.order_by('-created').select_related('kind')
    context = {'request': request}
    data = {}

    try:
        data['created'] = serializers.FruitSerializer(
            fruit.filter(created__gt=since, deleted=False).iterator(),
            context=context, many=True).data
        data['deleted'] = serializers.DeletedFruitSerializer(
            fruit.filter(created__gt=since, deleted=True).iterator(),
            context=context, many=True).data
        data['updated'] = serializers.FruitSerializer(
            fruit.filter(created__lte=since, modified__gt=since, deleted=False).iterator(),
            context=context, many=True).data

    except ValidationError as e:
        # nonsensical date/time
        return Response(
            data=dict(detail=e),
            status=status.HTTP_400_BAD_REQUEST,
        )

    return Response(data)
