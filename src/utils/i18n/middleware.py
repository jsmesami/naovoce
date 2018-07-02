from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class ForceDefaultLanguageMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if 'HTTP_ACCEPT_LANGUAGE' in request.META:
            del request.META['HTTP_ACCEPT_LANGUAGE']

        request.LANGUAGE_CODE = getattr(settings, 'LANGUAGE_CODE', 'en')
