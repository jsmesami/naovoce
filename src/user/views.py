from django.contrib.auth.decorators import login_required
from django.db.models import Count, Case, When
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from user.models import FruitUser


def index(request):
    pickers = FruitUser.objects\
        .filter(is_active=True, is_email_verified=True)\
        .exclude(username='fruitmap.sk')\
        .annotate(fruit_count=Count(Case(When(fruits__deleted=False, then=1))))\
        .order_by('-fruit_count', 'username')

    context = {
        'pickers': pickers.exclude(fruit_count=0),
        'others': pickers.filter(fruit_count=0),
    }

    return render(request, 'pickers/index.html', context)


def profile(request, pk, slug=None):
    user = get_object_or_404(FruitUser, pk=pk)

    if user.slug != slug:
        return HttpResponsePermanentRedirect(user.get_absolute_url())

    return render(request, 'pickers/detail.html', {'user': user})


accounts_profile = login_required(lambda r: HttpResponseRedirect(r.user.get_absolute_url()))
