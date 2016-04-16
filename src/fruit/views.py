from functools import wraps

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext, ugettext_lazy as _

from comments.utils import get_comments_context
from gallery.utils import get_gallery_context
from .forms import FruitForm, FruitDeleteForm
from .models import Fruit, Kind


def _get_fruit(pk):
    return get_object_or_404(Fruit.objects.select_related('user', 'kind'), pk=pk)


def detail(request, fruit_id):
    fruit = _get_fruit(fruit_id)
    context = {
        'kinds': Kind.objects.all(),
        'fruit': fruit,
    }
    context.update(get_comments_context(
        request,
        container=fruit,
        with_complaints=True,
        complaint_label=_('Send comment as a complaint'),
    ))
    context.update(get_gallery_context(
        request,
        container=fruit,
    ))

    return render(request, 'fruit/detail.html', context)


def add(request):
    if not request.user.is_authenticated():
        messages.warning(request, ugettext('To add markers, please first sign in.'))
        redir = '{}?next={}'.format(reverse('account_login'), reverse('fruit:add'))
        return HttpResponseRedirect(redir)

    if request.method == 'POST':
        form = FruitForm(request.POST)
        if form.is_valid():
            data = dict(user=request.user)
            data.update(form.cleaned_data)
            fruit = Fruit(**data)
            fruit.save()
            messages.success(request, ugettext('Thank you, the marker has been added.'))
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
        messages.success(request, ugettext('Thank you, your changes have been saved.'))
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
    if request.method == 'POST':
        form = FruitDeleteForm(request.POST)
        if form.is_valid():
            fruit.deleted = True
            fruit.why_deleted = form.cleaned_data['reason']
            fruit.save()
            messages.success(request, ugettext('The marker has been deleted.'))
            return redirect(fruit)
    else:
        form = FruitDeleteForm()

    context = {
        'form': form,
    }

    return render(request, 'fruit/delete.html', context)
