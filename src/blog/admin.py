from django.contrib import admin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from modeltranslation.admin import TranslationAdmin

from gallery.admin import ImageAdminInline, GalleryAdminMixin
from gallery.forms import CoverImageAdminForm
from .models import Category, BlogPost


class CategoryAdmin(TranslationAdmin):
    fields = 'name',
    list_display = 'name', '_blogs_count'
    list_filter = 'name',

    def _blogs_count(self, obj):
        return obj.blogposts.count()
    _blogs_count.short_description = _('blogs count')


class BlogPostAdmin(GalleryAdminMixin, TranslationAdmin):
    fields = 'title text categories public_from cover_image'.split()
    list_display = 'title author _is_public images_count created modified'.split()
    list_filter = 'categories__name',
    search_fields = 'title',
    ordering = '-created',
    readonly_fields = 'id',
    form = CoverImageAdminForm
    inlines = ImageAdminInline,

    def _is_public(self, obj):
        return obj.public_from <= timezone.now()
    _is_public.short_description = _('public')
    _is_public.boolean = True

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        obj.save()


admin.site.register(Category, CategoryAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
