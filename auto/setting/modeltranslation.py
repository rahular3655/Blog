gettext = lambda s: s

LANGUAGES = [
    ('en', gettext('English')),
    ('hi', gettext('Hindi')),
    ('ml', gettext('Malayalam')),
    ('zh-cn', gettext('Simplified Chinese')),
]

MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'

MODELTRANSLATION_FALLBACK_LANGUAGES = ('en', 'ml', 'hi', 'zh-cn')

MODELTRANSLATION_TRANSLATION_FILES = (
    'blogs.translation',
    'categories.translation',
    'statictext.translation',
)
