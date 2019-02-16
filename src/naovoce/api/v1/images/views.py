from fruit.models import Image
from rest_framework import generics

from ..permissions import IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly
from .serializers import ImageSerializer


class ImageDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or destroy specific Image resource."""

    queryset = Image.objects.select_related('author')
    serializer_class = ImageSerializer
    permission_classes = IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly


class ImageList(generics.ListCreateAPIView):
    """List or create Image resources."""

    serializer_class = ImageSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return Image.objects.filter(fruit=self.kwargs['fruit_pk']).select_related('author')

    def perform_create(self, serializer):
        kwargs = {
            'fruit_id': self.kwargs.pop('fruit_pk'),
            'author': self.request.user,
            **self.kwargs,
        }
        serializer.save(**kwargs)
