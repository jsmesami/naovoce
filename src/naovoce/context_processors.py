import os

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site


def common(request):
    return {
        'DEBUG': settings.DEBUG,
        'DOMAIN': get_current_site(request).domain,
        'RECAPTCHA_DISABLED': os.environ.get('RECAPTCHA_DISABLE')
    }
