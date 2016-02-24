from django.core.mail import mail_managers
from django.dispatch import receiver
from django.utils.translation import ugettext_noop, ugettext_lazy as _

from comments.signals import comment_created


@receiver(comment_created)
def somebody_commented_your_fruit(comment, comment_type, object_id, **kwargs):
    """
    Notify users that there has been some activity under their marker.
    """
    if comment_type.model == 'fruit':
        fruit = comment_type.get_object_for_this_type(pk=object_id)
        if fruit.user != comment.author:
            if not comment.complaint:
                msg_text = ugettext_noop(
                    'User <a href="{user_url}">{user_name}</a> '
                    'posted a <a href="{comment_url}">comment</a> '
                    'under your <a href="{fruit_url}">marker</a>.'
                )
            else:
                msg_text = ugettext_noop(
                    'User <a href="{user_url}">{user_name}</a> '
                    '<strong>posted a <a href="{comment_url}">complaint</a></strong> '
                    'under your <a href="{fruit_url}">marker</a>.'
                )
            comment_msg = msg_text.format(
                user_name=comment.author.username,
                user_url=comment.author.get_absolute_url(),
                comment_url=comment.get_absolute_url(),
                fruit_url=fruit.get_absolute_url(),
            )
            fruit.user.send_message(comment_msg, system=True)


@receiver(comment_created)
def complaint_notification(comment, *args, **kwargs):
    """
    Notify manages that complaint has been sent.
    """
    if comment.complaint:
        subject = _('A complaint has been made.')
        body = _('Please review the situation: https://na-ovoce.cz{url}'.format(
            url=comment.get_absolute_url(),
        ))
        mail_managers(subject, body)
