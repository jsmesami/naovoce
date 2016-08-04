from django.contrib import admin

from . import models


@admin.register(models.Upload)
class UploadAdmin(admin.ModelAdmin):
    model = models.Upload
    list_display = '_upload', '_url'

    def _upload(self, obj):
        return obj.title or str(obj)

    def _url(self, obj):
        return obj.file.url


@admin.register(models.Media)
class MediaAdmin(admin.ModelAdmin):
    model = models.Media
    list_display = 'name', 'date', 'type'
