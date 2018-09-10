# Save this file as local.py
from .base import *  # noqa

DEBUG = True
THUMBNAIL_DEBUG = DEBUG

# Allow localhost for development
ALLOWED_HOSTS = 'localhost',

SECRET_KEY = None  # Set a secret key!

# You may want to output emails to console:
# python -m smtpd -n -c DebuggingServer localhost:1025
EMAIL_PORT = 1025

# Make sure you loaded sites fixture
SITE_ID = 2

# Set correct credentials for development
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

NEWSLETTER_API_KEY = ''
NEWSLETTER_DEFAULT_LIST_ID = ''

# Disable cache
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

# Enable CORS for localhost
CORS_ORIGIN_WHITELIST += 'localhost:8000',

# on a Mac, syslog sits on a different path
# LOGGING['handlers']['syslog']['address'] = '/var/run/syslog'

# you may want to enable DRF browsable API
# REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
#     'rest_framework.renderers.JSONRenderer',
#     'rest_framework.renderers.BrowsableAPIRenderer',
# )
