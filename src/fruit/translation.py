from modeltranslation.translator import translator, TranslationOptions

from .models import Kind
from .herbarium.models import Herbarium, Season


class KindTranslationOptions(TranslationOptions):
    fields = 'name',


class HerbariumTranslationOptions(TranslationOptions):
    fields = 'full_name',


class SeasonTranslationOptions(TranslationOptions):
    fields = 'part',

translator.register(Kind, KindTranslationOptions)
translator.register(Herbarium, HerbariumTranslationOptions)
translator.register(Season, SeasonTranslationOptions)
