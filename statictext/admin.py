from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from modeltranslation.admin import TranslationTabularInline, TranslationAdmin

from common.media_mixins import MediaMixin
from .forms import RegulationsForm
from .models import StaticText, SocialMediaUrl, Regulations, CompanyDetails, DropDown, DropDownClass, FAQ, FaqCategory, FAQAnswer
from common.utils import CustomizedFormFieldMixin


# Register your models here.


class StaticTextAdmin(TranslationAdmin, CustomizedFormFieldMixin, MediaMixin):
    group_fieldsets = True

    list_filter = ('title',)

    search_fields = ('title',)

    list_display = ('title', 'slug',)

    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": ("title_en",)}


class SocialUrlInline(admin.TabularInline):
    model = SocialMediaUrl
    fields = ('name', 'url', 'image', 'is_active', 'thumbnail')
    readonly_fields = ('thumbnail',)
    extra = 1

    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="50px" />', obj.image.url)
        else:
            return 'No Image'


class CompanyDetailAdmin(CustomizedFormFieldMixin, TranslationAdmin, MediaMixin):
    list_display = ('name',)
    inlines = [SocialUrlInline]

    def has_add_permission(self, request):
        # Disable the 'Add' button
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class RegulationsAdmin(CustomizedFormFieldMixin, TranslationAdmin, MediaMixin):
    form = RegulationsForm
    group_fieldsets = True

    def has_add_permission(self, request):
        # Disable the 'Add' button
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def response_change(self, request, obj):
        # Override the response after changing an object
        if "_addanother" in request.POST:
            # Redirect to the add form again
            return super().response_change(request, obj)
        else:
            # Redirect to a custom URL or any other logic
            return HttpResponseRedirect(request.path)


class DropDownInline(TranslationTabularInline, MediaMixin):
    model = DropDown
    fields = ('value',)
    extra = 1


class DropDownClassAdmin(CustomizedFormFieldMixin, TranslationAdmin, MediaMixin):
    list_display = ('name', 'is_active')
    inlines = [DropDownInline]

    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": ("name_en",)}


class FAQAnswerInline(TranslationTabularInline, MediaMixin):
    model = FAQAnswer
    fields = ('answer',)
    extra = 0


class FAQAdmin(CustomizedFormFieldMixin, TranslationAdmin, MediaMixin):
    inlines = [FAQAnswerInline, ]
    list_display = ('question', 'is_active', 'created_at',)
    list_filter = ('question', 'created_at',)
    search_fields = ('question',)


class FAQCategoryAdmin(CustomizedFormFieldMixin, TranslationAdmin, MediaMixin):
    list_display = ('name', 'is_active', 'created_at',)
    list_filter = ('name', 'created_at', 'is_active',)
    search_fields = ('name',)

    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": ("name_en",)}


admin.site.register(StaticText, StaticTextAdmin)
admin.site.register(CompanyDetails, CompanyDetailAdmin)
admin.site.register(Regulations, RegulationsAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(FaqCategory, FAQCategoryAdmin)
admin.site.register(DropDownClass, DropDownClassAdmin)
