from typing import Any

from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from ajax_select.fields import autoselect_fields_check_can_add

from .filters import CustomSearchFilter
from accounts.admin import NonDeletedAuthorsAdminMixin
from common.media_mixins import MediaMixin
from common.utils import CustomizedFormFieldMixin
from .forms import BlogForm
from .models import Blog, BlogImage, BlogVideo


class BlogImageInline(TranslationTabularInline, MediaMixin):
    model = BlogImage

    readonly_fields = ('image_tag',)

    extra = 0


class BlogVideoInline(TranslationTabularInline, MediaMixin):
    model = BlogVideo

    extra = 0


class BlogAdmin(NonDeletedAuthorsAdminMixin, CustomizedFormFieldMixin, TranslationAdmin, MediaMixin):
    inlines = [BlogImageInline, BlogVideoInline]

    list_filter = ('user', 'published_on', 'unpublished_on', 'featured', 'is_popular', 'created_at',)

    search_fields = ('title',)

    form = BlogForm

    list_display = ('title', 'slug', 'user', 'created_at', 'published_on', 'unpublished_on', 'featured', 'is_popular', 'is_draft', 'is_live',)

    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": ("title_en",)}

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        qs = super().get_queryset(request)
        return qs.annotate_is_live()

    def is_live(self, obj):
        return obj.is_live

    def get_form(self, request, obj=None, **kwargs):  # to implement add button for user from blog instance.
        form = super().get_form(request, obj, **kwargs)
        autoselect_fields_check_can_add(form, self.model, request.user)
        return form


admin.site.register(Blog, BlogAdmin)
