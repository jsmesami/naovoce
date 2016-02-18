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

    top_pickers = pickers.exclude(username='fruitmap.sk')\
        .annotate(**fruit_counter).order_by('-fruit_count', 'username')[:10]

    fruit_count = Fruit.objects.valid().exclude(user__in=top_pickers).count()

    context = dict(
        top_pickers=top_pickers,
        pickers_count=pickers.count()-10,
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
