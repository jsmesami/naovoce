from django.conf import settings


def common(request):
    return {
        'DEBUG': settings.DEBUG
    }
