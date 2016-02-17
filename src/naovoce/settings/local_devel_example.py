# Save this file as local.py
from .base import *

DEBUG = True
THUMBNAIL_DEBUG = DEBUG

COMPRESS_ENABLED = False

SECRET_KEY = "**** Make this unique and don't share with anybody."

# you may want to output emails to console:
# python -m smtpd -n -c DebuggingServer localhost:1025
EMAIL_PORT = 1025

# make sure you loaded sites fixture
SITE_ID = 2

# Set correct credentials for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# disable cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    'fruit': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
}

# disable security features
SSL_ENABLED = False
SECURE_HSTS_SECONDS = 0
SECURE_CONTENT_TYPE_NOSNIFF = False
SECURE_BROWSER_XSS_FILTER = False
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
X_FRAME_OPTIONS = 'SAMEORIGIN'

# enable template debugging and disable caching
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG
TEMPLATES[0]['OPTIONS']['loaders'] = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]

# pip install django-debug-toolbar
# EXTERNAL_APPS = ('debug_toolbar',) + EXTERNAL_APPS

# on a Mac, syslog sits on a different path
# LOGGING['handlers']['syslog']['address'] = '/var/run/syslog'

# you may want to enable DRF browsable API
# REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
#     'rest_framework.renderers.JSONRenderer',
#     'rest_framework.renderers.BrowsableAPIRenderer',
# )
