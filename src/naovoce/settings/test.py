from .base import *  # noqa:F401,F403

DEBUG = True

SECRET_KEY = "dummy test key"

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "naovoce2",
        "USER": "test",
        "PASSWORD": "test",
        "HOST": "",
        "PORT": "",
    }
}

SECURE_SSL_REDIRECT = False

FRUIT_IMAGE_MAX_FILESIZE = 700

GDAL_LIBRARY_PATH = "/opt/homebrew/opt/gdal/lib/libgdal.dylib"
GEOS_LIBRARY_PATH = "/opt/homebrew/opt/geos/lib/libgeos_c.dylib"
