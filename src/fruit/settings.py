from django.conf import settings

FRUIT_IMAGE_MAX_FILESIZE = getattr(settings, 'FRUIT_IMAGE_MAX_FILESIZE', 5 * 1024 * 1024)
