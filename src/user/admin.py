from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from utils import trim_words

from .forms import MessageAdminForm, UserChangeForm, UserCreationForm
from .models import FacebookInfo, FruitUser, Message


class FacebookInfoInline(admin.TabularInline):
    model = FacebookInfo


@admin.register(FruitUser)
class FruitUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    fieldsets = (
        (None, {"fields": "username password".split()}),
        (
            _("Personal info"),
            {
                "fields": [
                    "first_name",
                    "last_name",
                    ("email", "is_email_verified"),
                    "external_url",
                    "motto",
                    "avatar",
                ],
            },
        ),
        (
            _("Permissions"),
            {
                "fields": "resolution is_active is_staff is_superuser " "groups user_permissions".split(),
            },
        ),
        (
            _("Important dates"),
            {
                "fields": "last_login date_joined".split(),
            },
        ),
    )

    list_display = (
        "username email first_name last_name " "is_staff is_active is_email_verified " "_has_facebook date_joined"
    ).split()

    list_filter = "resolution is_staff is_superuser is_active is_email_verified groups".split()

    add_fieldsets = (
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["username email password1 password2".split()],
            },
        ),
    )

    inlines = (FacebookInfoInline,)

    ordering = ("-date_joined",)

    def _has_facebook(self, obj):
        return bool(obj.facebook_info)

    _has_facebook.short_description = "fcb"
    _has_facebook.boolean = True


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    model = Message
    form = MessageAdminForm
    list_display = "_text created read system recipient".split()
    list_filter = "read system".split()
    search_fields = "recipient__username recipient__email".split()

    def _text(self, obj):
        return trim_words(obj.text, 80)

    _text.short_description = _("text")
