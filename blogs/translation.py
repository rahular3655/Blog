from modeltranslation.translator import translator, TranslationOptions

from blogs.models import Blog, BlogImage, BlogVideo


class BlogTranslationOptions(TranslationOptions):
    fields = ('title', 'short_description', 'content', 'alt_text',)


class BlogImageTranslationOptions(TranslationOptions):
    fields = ('alt_text',)


class BlogVideoTranslationOptions(TranslationOptions):
    fields = ('video', 'alt_text',)


translator.register(Blog, BlogTranslationOptions)
translator.register(BlogImage, BlogImageTranslationOptions)
translator.register(BlogVideo, BlogVideoTranslationOptions)
