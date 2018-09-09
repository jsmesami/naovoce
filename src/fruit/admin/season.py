from modeltranslation.admin import TranslationTabularInline

from fruit.herbarium.models import Season


class SeasonAdminInline(TranslationTabularInline):
    model = Season
    extra = 0
