from django.contrib import admin
from fruit.herbarium.models import Herbarium

from .season import SeasonAdminInline


class HerbariumAdmin(admin.ModelAdmin):
    model = Herbarium
    list_display = 'kind full_name latin_name'.split()
    inlines = (SeasonAdminInline,)
