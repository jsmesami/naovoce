from modeltranslation.translator import translator, TranslationOptions

from .models import Kind
from .herbarium.models import Herbarium


class KindTranslationOptions(TranslationOptions):
    fields = 'name',


class HerbariumTranslationOptions(TranslationOptions):
    fields = 'full_name',


translator.register(Kind, KindTranslationOptions)
translator.register(Herbarium, HerbariumTranslationOptions)
