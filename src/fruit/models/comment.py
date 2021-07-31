import logging

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _, ugettext_noop

from utils.models import TimeStampedModel

logger = logging.getLogger(__name__)

COMPLAINT_MSG = ugettext_noop(
    "User <a href='{user_url}'>{user_name}</a> "
    "<strong>posted a complaint</strong> under your <a href='{fruit_url}'>marker</a>."
)

COMMENT_MSG = ugettext_noop(
    "User <a href='{user_url}'>{user_name}</a> posted a comment under your <a href='{fruit_url}'>marker</a>."
)


class Comment(TimeStampedModel):
    text = models.CharField(_("comment"), max_length=1600)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("author"),
        related_name="comments",
        on_delete=models.CASCADE,
    )
    ip = models.GenericIPAddressField(_("author's IP address"), null=True)
    is_complaint = models.BooleanField(_("complaint"), default=False)
    is_rejected = models.BooleanField(_("rejected"), default=False)

    fruit = models.ForeignKey("fruit.Fruit", related_name="comments", on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment #{self.pk} by {self.author.username}"

    def save(self, **kwargs):
        if (fruit_user := self.fruit.user) != self.author:
            fruit_user.send_message(
                COMPLAINT_MSG if self.is_complaint else COMMENT_MSG,
                is_system=True,
                context=dict(
                    user_url=fruit_user.get_absolute_url(),
                    user_name=fruit_user.username,
                    fruit_url=self.fruit.get_absolute_url(),
                ),
            )

        super().save(**kwargs)

    @classmethod
    def post_create(cls, sender, instance, created, *args, **kwargs):
        if created:
            logger.info(
                "{what} on fruit {fruit_id} created by user {user!s} ({is_fruit_owner} fruit owner).".format(
                    what="Complaint" if instance.is_complaint else "Comment",
                    fruit_id=instance.fruit_id,
                    user=instance.author,
                    is_fruit_owner="IS" if instance.author == instance.fruit.user else "NOT",
                )
            )

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")
        ordering = ("-created",)


post_save.connect(Comment.post_create, sender=Comment)
