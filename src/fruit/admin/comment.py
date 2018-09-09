from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from fruit.models import Comment

from utils import trim_words


class CommentAdmin(admin.ModelAdmin):
    fields = 'text author ip is_complaint is_rejected'.split()
    readonly_fields = 'author ip'.split()
    list_display = '_text author is_complaint is_rejected'.split()
    search_fields = 'author__username author__email'.split()
    list_filter = 'is_complaint is_rejected'.split()

    def _text(self, obj):
        return trim_words(obj.text, 100)
    _text.short_description = _('text')


class CommentAdminInline(admin.TabularInline):
    model = Comment
    readonly_fields = 'author ip'.split()
    extra = 0
