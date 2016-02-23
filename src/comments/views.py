from ipware.ip import get_ip

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.utils.translation import ugettext

from utils.tokenizer import Token
from .models import Comment
from .forms import CommentForm
from . import signals


@require_POST
@login_required
def save(request):
    form = CommentForm(request.POST)

    if form.is_valid():
        comment_type = form.cleaned_data.get('content_type')
        object_id = form.cleaned_data.get('object_id')

        token = Token(comment_type.id, object_id)

        if request.POST.get('token') == str(token) and request.POST.get('tamper') == '':
            comment = Comment.objects.create(
                text=form.cleaned_data.get('text'),
                author=request.user,
                ip=get_ip(request),
                content_type=comment_type,
                object_id=object_id,
            )
            signals.comment_created.send(
                sender=Comment,
                comment=comment,
                comment_type=comment_type,
                object_id=object_id,
            )
            messages.success(request, ugettext('Thank you for your comment.'))
        else:
            return HttpResponseBadRequest('Invalid token')

    else:
        messages.error(request, ugettext('We are sorry, your comment was not accepted.'))

    return redirect(request.POST.get('next', '/'))
