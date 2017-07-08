from django.conf import settings


class ForceDefaultLanguageMiddleware:

    def process_request(self, request):
        if 'HTTP_ACCEPT_LANGUAGE' in request.META:
            del request.META['HTTP_ACCEPT_LANGUAGE']

        request.LANGUAGE_CODE = getattr(settings, 'LANGUAGE_CODE', 'en')
