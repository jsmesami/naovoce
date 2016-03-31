import sys

from rest_framework.serializers import HyperlinkedIdentityField

# used to cache URLS in CachedHyperlinkedIdentityField
URL_CACHE = {}


class CachedHyperlinkedIdentityField(HyperlinkedIdentityField):
    """
    This is a performance wrapper for HyperlinkedIdentityField.
    We save a ton of time by pre-computing the URL the first time it's
    accessed, to save calling reverse potentially thousands of times
    per request.
    """
    ID_TOKEN = str(sys.maxsize)

    def to_representation(self, value):
        global URL_CACHE
        try:
            url = URL_CACHE[self.view_name]
        except KeyError:
            real_id = value.id
            value.id = self.ID_TOKEN
            url = super(CachedHyperlinkedIdentityField, self).to_representation(value)
            URL_CACHE[self.view_name] = url
            value.id = real_id
        return url.replace(self.ID_TOKEN, str(value.id))




