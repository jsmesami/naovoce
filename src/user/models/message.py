from contextlib import suppress

from django.contrib.postgres.fields import HStoreField
from django.db import models
from django.utils.formats import date_format
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import pgettext_lazy, ugettext, ugettext_lazy as _

from utils.models import TimeStampedModel


class Message(TimeStampedModel):
    """Represents simple database-stored messages for users."""

    text = models.CharField(_("text"), max_length=255)
    context = HStoreField(
        _("context"),
        blank=True,
        null=True,
        help_text=_("Translation context for system messages"),
    )
    is_read = models.BooleanField(
        pgettext_lazy("user.Message", "read"),
        help_text=pgettext_lazy("Has been read or not.", "user.Message"),
        default=False,
    )
    is_system = models.BooleanField(
        pgettext_lazy("user.Message", "system"),
        help_text=_("System messages can be translated and can contain HTML."),
        default=False,
    )
    recipient = models.ForeignKey(
        "user.FruitUser",
        verbose_name=_("recipient"),
        related_name="messages",
        on_delete=models.CASCADE,
    )

    @property
    def text_formatted(self):
        text = ugettext(self.text)
        if self.is_system:
            if self.context:
                with suppress(KeyError):
                    text = format_html(text, **dict(self.context))
            else:
                text = mark_safe(text)

        return format_html(
            "<span class='date'>{date}</span> {text}",
            date=date_format(self.created, "SHORT_DATE_FORMAT", use_l10n=True),
            text=text,
        )

    def __str__(self):
        return self.text_formatted

    class Meta:
        ordering = ("-created",)
        verbose_name = _("message")
        verbose_name_plural = _("messages")
