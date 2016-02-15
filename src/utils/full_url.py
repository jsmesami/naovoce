from django.contrib.sites.models import get_current_site


def get_full_url(request, location):
    protocol = 'https://' if request.is_secure() else 'http://'
    return ''.join([protocol, get_current_site(request).domain, str(location)])
