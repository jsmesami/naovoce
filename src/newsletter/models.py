from urllib.parse import urlencode

import requests

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.models import TimeStampedModel


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


class List(TimeStampedModel):
    name = models.CharField(_('name'), max_length=255, unique=True)
    hash = models.CharField(_('hash'), max_length=255, unique=True)

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
        return cls.objects.filter(hash=settings.NEWSLETTER_DEFAULT_LIST_ID).first()

    def __str__(self):
        return '{s.name} ({s.hash})'.format(s=self)

    class Meta:
        verbose_name = _('recipient list')
        verbose_name_plural = _('recipient lists')
        ordering = '-created',


class Campaign(TimeStampedModel):
    subject = models.CharField(_('subject'), max_length=255)
    plain_text = models.TextField(_('plain text'))
    html_text = models.TextField(_('html text'))

    sent = models.BooleanField(_('sent'), default=False, editable=False)

    lists = models.ManyToManyField(
        List,
        verbose_name=_('subscriber lists'),
        related_name='campaigns',
    )

    from_name = models.CharField(
        _('from name'),
        max_length=255,
        default=settings.NEWSLETTER_DEFAULT_FROM_NAME,
    )

    from_email = models.EmailField(
        _('from email'),
        max_length=255,
        default=settings.NEWSLETTER_DEFAULT_FROM_EMAIL,
    )

    @property
    def query_string(self):
        return urlencode(dict(
            utm_source='na-ovoce.cz',
            utm_medium='newsletter',
            utm_campaign=self.subject,
        ))

    def __str__(self):
        return self.subject

    def create_draft(self):
        form = dict(
            api_key=settings.NEWSLETTER_API_KEY,
            from_name=self.from_name,
            from_email=self.from_email,
            reply_to=self.from_email,
            subject=self.subject,
            plain_text=self.plain_text,
            html_text=self.html_text,
            list_ids=','.join(self.lists.all().values_list('hash', flat=True)),
            brand_id=settings.NEWSLETTER_BRAND_ID,
            query_string=self.query_string,
            send_campaign=0,  # We do not send immediately.
        )
        ret = requests.post(API.create, data=form).content.decode()
        if not ret == 'Campaign created':
            raise ClientError(ret)
        else:
            return True

    def get_absolute_url(self):
        return reverse('newsletter:detail', args=[self.pk])

    class Meta:
        verbose_name = _('campaign')
        verbose_name_plural = _('campaigns')
        ordering = '-created',


class Asset(models.Model):
    campaign = models.ForeignKey(Campaign, verbose_name=_('campaign'), related_name='assets')

    def _upload_to(self, filename):
        return 'newsletter/{id}/{file}'.format(
            id=self.campaign_id,
            file=filename,
        )

    file = models.FileField(_('file'), upload_to=_upload_to)

    class Meta:
        verbose_name = _('asset')
        verbose_name_plural = _('assets')
