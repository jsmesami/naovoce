from django.core.mail import mail_managers
from django.dispatch import receiver
from django.utils.translation import ugettext_noop, ugettext_lazy as _

from comments.signals import comment_created
from gallery.signals import image_created


@receiver(comment_created)
def somebody_commented_your_fruit(comment, comment_type, object_id, **kwargs):
    """
    Notify users that there is a new comment under their marker.
    """
    if comment_type.model == 'fruit':
        fruit = comment_type.get_object_for_this_type(pk=object_id)
        if fruit.user != comment.author:
            if not comment.complaint:
                msg_template = ugettext_noop(
                    'User <a href="{user_url}">{user_name}</a> '
                    'posted a <a href="{comment_url}">comment</a> '
                    'under your <a href="{fruit_url}">marker</a>.'
                )
            else:
                msg_template = ugettext_noop(
                    'User <a href="{user_url}">{user_name}</a> '
                    '<strong>posted a <a href="{comment_url}">complaint</a></strong> '
                    'under your <a href="{fruit_url}">marker</a>.'
                )
            msg = msg_template.format(
                user_name=comment.author.username,
                user_url=comment.author.get_absolute_url(),
                comment_url=comment.get_absolute_url(),
                fruit_url=fruit.get_absolute_url(),
            )
            fruit.user.send_message(msg, system=True)


@receiver(comment_created)
def complaint_notification(comment, *args, **kwargs):
    """
    Notify manages that complaint has been sent.
    """
    if comment.complaint:
        subject = _('A complaint has been made.')
        body = _('Please review the situation: https://na-ovoce.cz{url}').format(
            url=comment.get_absolute_url(),
        )
        mail_managers(subject, body)


@receiver(image_created)
def somebody_added_image_to_your_fruit(image, gallery_ct, gallery_id, **kwargs):
    """
    Notify users that somebody added an image to their marker.
    """
    if gallery_ct.model == 'fruit':
        fruit = gallery_ct.get_object_for_this_type(pk=gallery_id)
        if fruit.user != image.author:
            msg_template = ugettext_noop(
                'User <a href="{user_url}">{user_name}</a> '
                'added a <a href="{image_url}">photo</a> '
                'under your <a href="{fruit_url}">marker</a>.'
            )
            msg = msg_template.format(
                user_name=image.author.username,
                user_url=image.author.get_absolute_url(),
                image_url=image.get_absolute_url(),
                fruit_url=fruit.get_absolute_url(),
            )
            fruit.user.send_message(msg, system=True)
