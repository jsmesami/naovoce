from django.contrib import admin

from fruit.models import Image


class ImageAdmin(admin.ModelAdmin):
    fields = 'image author caption'.split()
    readonly_fields = 'author',
    list_display = '__str__ author caption'.split()


class ImageAdminInline(admin.TabularInline):
    model = Image
    readonly_fields = 'author',
    extra = 0
