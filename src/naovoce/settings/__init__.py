try:
    from .local import *
except ImportError:
    raise ImproperlyConfigured('Please provide instance-specific settings/local.py '
                               '(see settings/local_example.py).')

if SECRET_KEY.startswith('****'):
    from django.core.exceptions import ImproperlyConfigured
    raise ImproperlyConfigured('Please set SECRET_KEY in settings/local.py '
                               'to a unique, unpredictable value.')

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + EXTERNAL_APPS + ADMIN_APPS
