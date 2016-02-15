"""
WSGI config for naovoce project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application


os.environ['HTTPS'] = 'on'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "naovoce.settings")

application = get_wsgi_application()
