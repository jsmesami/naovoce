from fruit.herbarium.models import Season
from modeltranslation.admin import TranslationTabularInline


class SeasonAdminInline(TranslationTabularInline):
    model = Season
    extra = 0
