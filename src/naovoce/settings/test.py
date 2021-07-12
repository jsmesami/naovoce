from .base import *  # noqa:F401,F403

DEBUG = True

SECRET_KEY = "dummy test key"

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "naovoce",
        "USER": "test",
        "PASSWORD": "test",
        "HOST": "",
        "PORT": "",
    }
}

SECURE_SSL_REDIRECT = False

FRUIT_IMAGE_MAX_FILESIZE = 700
