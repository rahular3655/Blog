from modeltranslation.translator import translator, TranslationOptions

from categories.models import Category


class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'alt_text',)



translator.register(Category, CategoryTranslationOptions)
