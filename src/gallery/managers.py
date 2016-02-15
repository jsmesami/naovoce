from django.db import models


class GalleryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related('images')
