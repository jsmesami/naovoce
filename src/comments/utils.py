from ipware.ip import get_ip

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext, ugettext_lazy as _

from utils.tokenizer import Token
from .models import Comment
from .forms import comment_form_factory
from . import signals


def get_comments_context(request, container, with_complaints=False, complaint_label=None):
    """
    Returns additional context for comments-handling views.
    """

    comment_type = ContentType.objects.get_for_model(container)
    token = str(Token(comment_type.id, container.id))

    CommentForm = comment_form_factory(with_complaints, complaint_label)

    if request.method == 'POST':
        if request.user.is_authenticated():
            form = CommentForm(request.POST)
            if form.is_valid():
                is_complaint = form.cleaned_data.get('complaint', False)
                if request.POST.get('token') == token:
                    comment = Comment.objects.create(
                        text=form.cleaned_data.get('text'),
                        complaint=is_complaint,
                        author=request.user,
                        ip=get_ip(request),
                        content_type=comment_type,
                        object_id=container.id,
                    )
                    form = CommentForm()
                    signals.comment_created.send(
                        sender=Comment,
                        comment=comment,
                        comment_type=comment_type,
                        object_id=container.id,
                    )
                    if is_complaint:
                        messages.error(request, ugettext('Your complaint has been sent to'
                                                         ' site administrators.'))
                    else:
                        messages.success(request, ugettext('Thank you for your comment.'))
                else:
                    form.add_error(None, _('Comment not accepted.'))
        else:
            form = CommentForm()
            messages.error(request, ugettext('You have to be signed-in to post comments.'))
    else:
        form = CommentForm()

    return {
        'comment_form': form,
        'token': token,
        'comments': Comment.objects.filter(
            content_type=comment_type,
            object_id=container.id,
        ).prefetch_related('author'),
    }
