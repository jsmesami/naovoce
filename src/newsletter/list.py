import requests
from django.conf import settings


def create_urls(**kwargs):
    base_url = settings.NEWSLETTER_INSTALLATION_URL
    return type("API", (), {k: base_url + v for k, v in kwargs.items()})


API = create_urls(
    create="/api/campaigns/create.php",
    subscribe="/subscribe",
    unsubscribe="/unsubscribe",
    status="/api/subscribers/subscription-status.php",
    count="/api/subscribers/active-subscriber-count.php",
)


class ClientError(RuntimeError):
    pass


class DummyList:
    def subscribe(self, user):
        pass

    def unsubscribe(self, user):
        pass

    def subscription_status(self, user):
        pass

    def is_subscribed(self, user):
        pass


class List:
    def __init__(self, list_id):
        self.hash = list_id

    def subscribe(self, user):
        form = dict(
            email=user.email,
            list=self.hash,
            boolean="true",  # Request plaintext response.
        )
        ret = requests.post(API.subscribe, data=form).content.decode()

        if ret != "1":
            raise ClientError(ret)

        return True

    def unsubscribe(self, user):
        form = dict(
            email=user.email,
            list=self.hash,
            boolean="true",  # Request plaintext response.
        )
        ret = requests.post(API.unsubscribe, data=form).content.decode()

        if ret != "1":
            raise ClientError(ret)

        return True

    def subscription_status(self, user):
        form = dict(
            api_key=settings.NEWSLETTER_API_KEY,
            email=user.email,
            list_id=self.hash,
        )
        return requests.post(API.status, data=form).content.decode()

    def is_subscribed(self, user):
        ret = self.subscription_status(user)

        if ret == "Subscribed":
            return True
        elif ret in ("Email does not exist in list", "Unsubscribed"):  # noqa:SIM106
            return False
        else:
            raise ClientError(ret)


DEFAULT_LIST = DummyList() if settings.NEWSLETTER_DEBUG else List(settings.NEWSLETTER_DEFAULT_LIST_ID)
