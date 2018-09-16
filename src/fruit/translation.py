from modeltranslation.translator import TranslationOptions, translator

from .models import Kind


class KindTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(Kind, KindTranslationOptions)
