# Save this file as local.py
from .base import *  # noqa

SECRET_KEY = "faketestkey"

# Set correct credentials for production
SERVER_EMAIL = ''
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

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

NEWSLETTER_API_KEY = '****'
NEWSLETTER_DEFAULT_LIST_ID = '****'

SECURE_SSL_REDIRECT = False
