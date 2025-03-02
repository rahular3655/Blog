from modeltranslation.translator import translator, TranslationOptions

from .models import Tag


class TagTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)


translator.register(Tag, TagTranslationOptions)
