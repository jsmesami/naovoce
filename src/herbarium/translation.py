from modeltranslation.translator import TranslationOptions, translator

from .models import Herbarium, Season


class HerbariumTranslationOptions(TranslationOptions):
    fields = ('full_name',)


class SeasonTranslationOptions(TranslationOptions):
    fields = ('part',)


translator.register(Herbarium, HerbariumTranslationOptions)
translator.register(Season, SeasonTranslationOptions)
