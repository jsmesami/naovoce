import hashlib

from django.conf import settings


class Token:
    def __init__(self, *data):
        s = settings.SECRET_KEY+''.join(str(chunk) for chunk in data)
        self.token = hashlib.sha512(s.encode('utf-8')).hexdigest()

    def __str__(self):
        return self.token
