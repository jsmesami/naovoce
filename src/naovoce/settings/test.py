from .base import *  # noqa pylint: disable=W0401,W0614

SECRET_KEY = 'dummy test key'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'travis_ci_test',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

SECURE_SSL_REDIRECT = False
