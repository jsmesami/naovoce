import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Case, When
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from fruit.models import Kind, Fruit
from user.models import FruitUser


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
