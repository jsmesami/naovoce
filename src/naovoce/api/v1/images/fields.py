import base64
import binascii
import imghdr

from django.core.files.base import ContentFile
from rest_framework import serializers


class Base64ImageField(serializers.ImageField):
    """Field that handles base64 image data."""

    def to_internal_value(self, data):
        if isinstance(data, str):
            if "data:" in data and ";base64," in data:
                header, data = data.split(";base64,")

            try:
                decoded_data = base64.b64decode(data)
            except (TypeError, binascii.Error):
                self.fail("invalid_image")

            file_name = "uploaded_image." + self.guess_file_extension(decoded_data)

            data = ContentFile(decoded_data, name=file_name)

        return super().to_internal_value(data)

    @staticmethod
    def guess_file_extension(image_data):
        extension = imghdr.what(None, image_data)
        return extension.lower() if extension else "jpg"
