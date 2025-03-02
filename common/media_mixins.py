"""
Mixin to provide a good interface in admin panel for model translations - 
Used in admin.py in all apps that used model translation.
"""


class MediaMixin:
    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css', '/static/froala_editor/css/froala_custom.css',
                       'https://fonts.googleapis.com/css?family=Manrope:400,400italic,400italic,700,700italic&subset=latin,vietnamese,latin-ext,cyrillic,cyrillic-ext,greek-ext,greek'),
        }
