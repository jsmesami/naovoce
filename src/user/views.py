import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, Case, When
from django.http import (
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
    Http404,
)
from django.shortcuts import get_object_or_404, render
from django.views.generic.edit import UpdateView
from django.utils.translation import ugettext_lazy as _

from fruit.models import Kind, Fruit
from user.forms import UserSettingsForm
from user.models import FruitUser
from utils.mixins import LoginRequiredMixin


def fruit_counter(**filters):
    return {
        'fruit_count': Count(Case(When(fruits__deleted=False, then=1, **filters)))
    }


def _get_pickers(**filters):
    return FruitUser.objects.active()\
        .exclude(username='fruitmap.sk')\
        .filter(**filters)\
        .annotate(**fruit_counter(**filters))\
        .order_by('-fruit_count', 'username')


def index(request):
    top_all_time = _get_pickers()

    last_month = datetime.date.today() - datetime.timedelta(365/12)
    top_last_month = _get_pickers(fruits__created__gte=last_month).exclude(fruit_count=0)

    context = dict(
        top_all_time=top_all_time[:10],
        top_last_month=top_last_month[:4],
        pickers_count=FruitUser.objects.active().order_by().count(),
        fruit_count=Fruit.objects.valid().order_by().count(),
    )

    return render(request, 'pickers/index.html', context)


def profile(request, pk, slug=None):
    qs = FruitUser.objects.annotate(**fruit_counter())

    user = get_object_or_404(qs, pk=pk)

    if user.slug != slug:
        return HttpResponsePermanentRedirect(user.get_absolute_url())

    return render(request, 'pickers/detail.html', {
        'user': user,
        'kinds': Kind.objects.all(),
    })


# This is here because of Allauth (we don't want two different user profile urls).
accounts_profile = login_required(lambda r: HttpResponseRedirect(r.user.get_absolute_url()))


@login_required
def messages(request, pk):
    qs = FruitUser.objects.prefetch_related('messages')

    user = get_object_or_404(qs, pk=pk)

    if user != request.user:
        raise Http404

    response = render(request, 'pickers/messages.html', {
        'user': user,
    })
    # We have rendered the response to show unread messages,
    # then marking them read for subsequent pageviews.
    user.clear_messages()
    return response


class UserSettingsView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    template_name = 'pickers/settings.html'
    model = FruitUser
    form_class = UserSettingsForm
    success_message = _('Settings successfully updated.')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
