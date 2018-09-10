from django.core.exceptions import ImproperlyConfigured

try:
    from .local import *  # noqa pylint: disable=W0401,W0614
except ImportError:
    raise ImproperlyConfigured('Please provide instance-specific settings/local.py '
                               '(see settings/local_[prod|dev]_example.py).')

if SECRET_KEY is None:
    raise ImproperlyConfigured('Please set SECRET_KEY in settings/local.py '
                               'to a unique, unpredictable value.')
