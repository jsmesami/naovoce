from .base import *  # pylint: disable=W0401,W0614

DEBUG = True

SECRET_KEY = 'dummy test key'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'naovoce',
        'USER': 'test',
        'PASSWORD': 'test',
        'HOST': '',
        'PORT': '',
    }
}

SECURE_SSL_REDIRECT = False
