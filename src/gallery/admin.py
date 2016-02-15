from django.contrib import admin
from django.contrib.contenttypes.generic import GenericTabularInline
from django.utils.translation import ugettext_lazy as _

from .models import Image


class ImageAdmin(admin.ModelAdmin):
    fields = 'image caption'.split()
    list_display = '__str__ author gallery_ct'.split()


class ImageAdminInline(GenericTabularInline):
    model = Image
    ct_field = 'gallery_ct'
    ct_fk_field = 'gallery_id'
    readonly_fields = 'pk',
    allow_add = True
    extra = 0


admin.site.register(Image, ImageAdmin)


class GalleryAdminMixin:
    def save_formset(self, request, form, formset, change):
        if formset.model == Image:
            instances = formset.save(commit=False)
            for instance in instances:
                if not instance.author:
                    instance.author = request.user
                instance.save()
            formset.save_m2m()
            return instances
        else:
            return formset.save()

    def images_count(self, obj):
        return obj.images.count()
    images_count.short_description = _('images')
