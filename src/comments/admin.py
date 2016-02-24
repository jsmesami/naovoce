from django.contrib import admin
from django.contrib.contenttypes.generic import GenericTabularInline
from django.utils.translation import ugettext_lazy as _

from utils import trim_words

from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    fields = 'text author ip complaint rejected'.split()
    list_display = '_text author _container complaint rejected'.split()
    search_fields = 'author__username author__email'.split()
    list_filter = 'complaint rejected'.split()

    def _text(self, obj):
        return trim_words(obj.text, 100)
    _text.short_description = _('text')

    def _container(self, obj):
        return obj.content_type
    _container.short_description = _('container')
    _container.admin_order_field = 'content_type'

    def has_add_permission(self, request):
        return False


class CommentAdminInline(GenericTabularInline):
    model = Comment


admin.site.register(Comment, CommentAdmin)
