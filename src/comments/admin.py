from django.contrib import admin
from django.contrib.contenttypes.generic import GenericTabularInline
from django.utils.translation import ugettext_lazy as _

from utils import trim_words

from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    fields = 'text author ip rejected'.split()
    list_display = '_text author _container rejected'.split()

    def _text(self, obj):
        return trim_words(obj.text, 100)
    _text.short_description = _('text')

    def _container(self, obj):
        return obj.content_type
    _container.short_description = _('container')

    def has_add_permission(self, request):
        return False


class CommentAdminInline(GenericTabularInline):
    model = Comment


admin.site.register(Comment, CommentAdmin)
