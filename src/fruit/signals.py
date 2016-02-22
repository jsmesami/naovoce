from django.dispatch import receiver
from django.utils.translation import ugettext_noop

from comments.signals import comment_created


@receiver(comment_created)
def somebody_commented_your_fruit(comment, comment_type, object_id, **kwargs):
    """
    Notify users that there has been some activity under their marker.
    """
    if comment_type.model == 'fruit':
        fruit = comment_type.get_object_for_this_type(pk=object_id)
        if fruit.user != comment.author:
            comment_msg = ugettext_noop(
                'User <a href="{user_url}">{user_name}</a> '
                'posted a <a href="{comment_url}">comment</a> '
                'under your <a href="{fruit_url}">marker</a>.'.format(
                    user_name=comment.author.username,
                    user_url=comment.author.get_absolute_url(),
                    comment_url=comment.get_absolute_url(),
                    fruit_url=fruit.get_absolute_url(),
                )
            )
            fruit.user.send_message(comment_msg, system=True)
