from django.conf import settings

# Iterable of lowercase model names, whose instances are allowed to store images
# POSTed by authenticated users (default is empty list).
GALLERY_PUBLIC_CONTAINERS = getattr(settings, 'GALLERY_PUBLIC_CONTAINERS', [])

# Integer number of maximum bytes available for image storage (default is 5MB).
GALLERY_IMAGE_MAX_FILESIZE = getattr(settings, 'GALLERY_IMAGE_MAX_FILESIZE', 5 * 1024 * 1024)
