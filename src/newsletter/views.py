import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_POST

from user.models import FruitUser
from .list import List, ClientError

logger = logging.getLogger(__name__)


@require_POST
@login_required
def subscribtion(request, user_pk):
    user = get_object_or_404(FruitUser, pk=user_pk)
    mailing_list = List.get_default()

    if 'subscribe' in request.POST:
        try:
            mailing_list.subscribe(user)
            messages.info(request, _('You have been successfully subscribed to our newsletter.'))
        except (ClientError, AttributeError) as e:
            messages.error(request, _('There has been an error subscribing you to our newsletter.'))
            logger.error('Error subscribing {} to the newsletter ({}).'.format(user.email, e))

    elif 'unsubscribe' in request.POST:
        try:
            mailing_list.unsubscribe(user)
            messages.info(request, _('You have been successfully unsubscribed from our newsletter.'))
        except (ClientError, AttributeError) as e:
            messages.error(request, _('There has been an error unsubscribing you from our newsletter.'))
            logger.error('Error unsubscribing {} from the newsletter ({}).'.format(user.email, e))

    return HttpResponseRedirect(reverse('pickers:settings', args=[user.pk]))
