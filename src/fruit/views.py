from functools import wraps

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext_lazy as _

from .forms import FruitForm
from .models import Fruit, Kind


def _get_fruit(pk):
    return get_object_or_404(Fruit.objects.select_related('user', 'kind'), pk=pk)


def detail(request, fruit_id):
    context = {
        'kinds': Kind.objects.all(),
        'fruit': _get_fruit(fruit_id),
    }
    return render(request, 'fruit/detail.html', context)


def add(request):
    if not request.user.is_authenticated():
        messages.warning(request, _('To add fruit, please first sign in.'))
        redir = '{}?next={}'.format(reverse('account_login'), reverse('fruit:add'))
        return HttpResponseRedirect(redir)

    if request.method == 'POST':
        form = FruitForm(request.POST)
        if form.is_valid():
            data = dict(user=request.user)
            data.update(form.cleaned_data)
            fruit = Fruit(**data)
            fruit.save()
            messages.success(request, _('Thank you, the fruit has been added.'))
            return redirect(fruit)
    else:
        form = FruitForm()

    context = {
        'kinds': Kind.objects.all(),
        'form': form,
    }

    return render(request, 'fruit/add.html', context)


def _editor(func):
    @wraps(func)
    def test(request, fruit_id):
        fruit = _get_fruit(fruit_id)

        if not (fruit.user.id == request.user.id):
            return HttpResponseForbidden(_('Only the owner is allowed edit her marker.'))

        if fruit.deleted:
            return HttpResponseForbidden(_('This marker has been deleted and cannot be edited.'))

        return func(request, fruit)

    return test


@login_required
@_editor
def edit(request, fruit):
    form = FruitForm(request.POST or None, instance=fruit)

    if form.is_valid():
        form.save()
        messages.success(request, _('Thank you, your changes have been saved.'))
        return redirect(fruit)

    context = {
        'kinds': Kind.objects.all(),
        'fruit': fruit,
        'form': form,
    }

    return render(request, 'fruit/edit.html', context)


@login_required
@_editor
def delete(request, fruit):
    redirect_to = reverse('fruit:add')

    if request.method == 'POST':
        fruit.deleted = True
        fruit.save()
        messages.success(request, _('The marker has been deleted.'))
        return redirect(redirect_to)

    message = _('Are you sure you want to delete this marker?'
                ' {fruit.kind.name} ({fruit.latitude:.4f}, {fruit.longitude:.4f})')

    context = {
        'next': redirect_to,
        'back': reverse('fruit:detail', args=[fruit.id]),
        'message': message.format(fruit=fruit)
    }

    return render(request, 'fruit/delete.html', context)
