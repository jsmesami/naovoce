from django.conf import settings
import requests


def create_urls(**kwargs):
    base_url = settings.NEWSLETTER_INSTALLATION_URL
    return type('API', (), {k: base_url + v for k, v in kwargs.items()})


API = create_urls(
    create='/api/campaigns/create.php',
    subscribe='/subscribe',
    unsubscribe='/unsubscribe',
    status='/api/subscribers/subscription-status.php',
    count='/api/subscribers/active-subscriber-count.php',
)


class ClientError(RuntimeError):
    pass


class List:

    def __init__(self, list_id):
        self.hash = list_id

    def subscribe(self, user):
        form = dict(
            email=user.email,
            list=self.hash,
            boolean='true',  # Request plaintext response.
        )
        ret = requests.post(API.subscribe, data=form).content.decode()

        if ret == '1':
            return True
        else:
            raise ClientError(ret)

    def unsubscribe(self, user):
        form = dict(
            email=user.email,
            list=self.hash,
            boolean='true',  # Request plaintext response.
        )
        ret = requests.post(API.unsubscribe, data=form).content.decode()

        if ret == '1':
            return True
        else:
            raise ClientError(ret)

    def is_subscribed(self, user):
        form = dict(
            api_key=settings.NEWSLETTER_API_KEY,
            email=user.email,
            list_id=self.hash,
        )
        ret = requests.post(API.status, data=form).content.decode()

        if ret == 'Subscribed':
            return True
        elif ret in ('Email does not exist in list', 'Unsubscribed'):
            return False
        else:
            raise ClientError(ret)

    @classmethod
    def get_default(cls):
        return cls(settings.NEWSLETTER_DEFAULT_LIST_ID)
