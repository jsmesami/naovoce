import re

from django.conf import settings
from django.utils.cache import patch_vary_headers
from django.utils import translation


LANG_PREFIX_RE = re.compile(r'^/({codes})/'.format(codes='|'.join(dict(settings.LANGUAGES).keys())))


class SessionBasedLocaleMiddleware:
    """
    This Middleware saves language in path into user session, so that subsequent urls
    without language prefix and error messages are rendered with correct translation.
    """

    def __lang_in_path(self, pth):
        match = re.match(LANG_PREFIX_RE, pth)

        return match.group(1) if match else None

    def process_request(self, request):
        lang = self.__lang_in_path(request.path)

        if lang and request.method == 'GET':
            request.session['language'] = lang
        else:
            lang = request.session.get('language') or \
                   translation.get_language_from_request(request)

        translation.activate(lang)
        request.LANGUAGE_CODE = translation.get_language()

    def process_response(self, request, response):
        patch_vary_headers(response, ('Accept-Language',))

        if 'Content-Language' not in response:
            response['Content-Language'] = translation.get_language()

        translation.deactivate()

        return response
