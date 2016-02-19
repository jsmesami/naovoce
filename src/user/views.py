import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Case, When
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from fruit.models import Kind, Fruit
from user.models import FruitUser

fruit_counter = {
    'fruit_count': Count(Case(When(fruits__deleted=False, then=1)))
}


def index(request):
    pickers = FruitUser.objects.filter(is_active=True, is_email_verified=True)

    top_all_time = pickers.exclude(username='fruitmap.sk')\
        .annotate(**fruit_counter).order_by('-fruit_count', 'username')

    last_month = datetime.date.today() - datetime.timedelta(365/12)
    top_last_month = top_all_time.filter(fruits__created__gte=last_month)

    fruit_count = Fruit.objects.valid().count()

    context = dict(
        top_all_time=top_all_time[:10],
        top_last_month=top_last_month[:4],
        pickers_count=pickers.count(),
        fruit_count=fruit_count,
    )

    return render(request, 'pickers/index.html', context)


def profile(request, pk, slug=None):
    qs = FruitUser.objects.annotate(**fruit_counter)

    user = get_object_or_404(qs, pk=pk)

    if user.slug != slug:
        return HttpResponsePermanentRedirect(user.get_absolute_url())

    return render(request, 'pickers/detail.html', {
        'user': user,
        'kinds': Kind.objects.all(),
    })


accounts_profile = login_required(lambda r: HttpResponseRedirect(r.user.get_absolute_url()))
