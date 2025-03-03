from modeltranslation.translator import translator, TranslationOptions

from .models import StaticText, CompanyDetails, FAQ, DropDownClass, DropDown, Regulations, FaqCategory, FAQAnswer


class StaticTextTranslationOptions(TranslationOptions):
    fields = ('title',)


class CompanyTranslationOptions(TranslationOptions):
    fields = ('name', 'address',)


class RegulationsTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'value',)


class DropDownClassTranslationOptions(TranslationOptions):
    fields = ('name',)


class DropDownTranslationOptions(TranslationOptions):
    fields = ('value',)


class FAQTranslationOptions(TranslationOptions):
    fields = ('question',)


class FAQAnswerTranslationOptions(TranslationOptions):
    fields = ('answer',)


class FAQCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(StaticText, StaticTextTranslationOptions)
translator.register(Regulations, RegulationsTranslationOptions)
translator.register(CompanyDetails, CompanyTranslationOptions)
translator.register(DropDownClass, DropDownClassTranslationOptions)
translator.register(DropDown, DropDownTranslationOptions)
translator.register(FAQ, FAQTranslationOptions)
translator.register(FAQAnswer, FAQAnswerTranslationOptions)
translator.register(FaqCategory, FAQCategoryTranslationOptions)
