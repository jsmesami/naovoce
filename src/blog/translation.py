from modeltranslation.translator import translator, TranslationOptions
from .models import Category, BlogPost


class CategoryTranslationOptions(TranslationOptions):
    fields = 'name',


class BlogPostTranslationOptions(TranslationOptions):
    fields = 'title', 'text',


translator.register(Category, CategoryTranslationOptions)
translator.register(BlogPost, BlogPostTranslationOptions)
