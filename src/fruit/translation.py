from modeltranslation.translator import TranslationOptions, translator

from .herbarium.models import Herbarium, Season
from .models import Kind


class KindTranslationOptions(TranslationOptions):
    fields = 'name',


class HerbariumTranslationOptions(TranslationOptions):
    fields = 'full_name',


class SeasonTranslationOptions(TranslationOptions):
    fields = 'part',


translator.register(Kind, KindTranslationOptions)
translator.register(Herbarium, HerbariumTranslationOptions)
translator.register(Season, SeasonTranslationOptions)
