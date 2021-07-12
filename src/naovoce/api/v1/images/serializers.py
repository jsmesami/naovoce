from functools import partial

from django.conf import settings
from rest_framework import serializers

from fruit.models import Image

from ..users.serializers import UserSerializer
from ..validators import validate_file_size, validate_file_type
from .fields import Base64ImageField


class ImageSerializer(serializers.HyperlinkedModelSerializer):

    image = Base64ImageField(
        validators=[
            partial(
                validate_file_type,
                content_types=settings.FRUIT_IMAGE_ALLOWED_CONTENT_TYPES,
            ),
            partial(validate_file_size, max_filesize=settings.FRUIT_IMAGE_MAX_FILESIZE),
        ]
    )

    author = UserSerializer(read_only=True)

    class Meta:
        model = Image
        fields = "id image caption author".split()
