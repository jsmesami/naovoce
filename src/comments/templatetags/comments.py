from django.contrib.contenttypes.models import ContentType
from django.template.base import Library

from utils.tokenizer import Token
from comments.models import Comment
from comments.forms import CommentForm

register = Library()


@register.inclusion_tag('comments/comments.html', takes_context=True)
def comments_for(context, container):
    comment_type = ContentType.objects.get_for_model(container)

    context.update({
        'comments': Comment.objects.filter(
            content_type=comment_type,
            object_id=container.id,
        ).prefetch_related('author'),
        'form': CommentForm(initial=dict(
            content_type=comment_type,
            object_id=container.id,
        )),
        'token': Token(comment_type.id, container.id),
    })

    return context
