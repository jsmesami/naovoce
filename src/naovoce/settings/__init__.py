from django.core.exceptions import ImproperlyConfigured

try:
    from .local import *  # noqa
except ImportError:
    raise ImproperlyConfigured('Please provide instance-specific settings/local.py '
                               '(see settings/local_[prod|dev]_example.py).')

if SECRET_KEY is None:
    from django.core.exceptions import ImproperlyConfigured
    raise ImproperlyConfigured('Please set SECRET_KEY in settings/local.py '
                               'to a unique, unpredictable value.')
