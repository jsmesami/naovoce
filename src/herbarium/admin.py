from django.contrib import admin
from modeltranslation.admin import TranslationTabularInline

from .models import Herbarium, Season


class SeasonAdminInline(TranslationTabularInline):
    model = Season
    extra = 0


class HerbariumAdmin(admin.ModelAdmin):
    model = Herbarium
    list_display = 'kind full_name latin_name'.split()
    inlines = (SeasonAdminInline,)


admin.site.register(Herbarium, HerbariumAdmin)
