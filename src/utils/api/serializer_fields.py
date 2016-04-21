import sys

from rest_framework.serializers import HyperlinkedIdentityField


class CachedHyperlinkedIdentityField(HyperlinkedIdentityField):
    """
    This is a performance wrapper for HyperlinkedIdentityField.
    We save a ton of time by pre-computing the URL the first time it's
    accessed, to save calling reverse potentially thousands of times
    per request.
    nb. we are not using cache here because of performance.
    """
    ID_TOKEN = str(sys.maxsize)
    URL_CACHE = {}

    def to_representation(self, value):
        cache_key = self.view_name
        url = self.URL_CACHE.get(cache_key)
        if not url:
            real_id = value.id
            value.id = self.ID_TOKEN
            url = super().to_representation(value)
            self.URL_CACHE[cache_key] = url
            value.id = real_id
        return url.replace(self.ID_TOKEN, str(value.id))
