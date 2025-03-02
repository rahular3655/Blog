from modeltranslation.translator import translator, TranslationOptions

from categories.models import Category, TrainingCategory


class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'alt_text',)


class TrainingCategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'alt_text',)


translator.register(Category, CategoryTranslationOptions)
translator.register(TrainingCategory, TrainingCategoryTranslationOptions)
