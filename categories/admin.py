from django.contrib import admin
from django.contrib.admin.widgets import AdminTextInputWidget
from django.db.models import Count
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from modeltranslation.admin import TranslationAdmin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from common.media_mixins import MediaMixin
from common.utils import CustomizedFormFieldMixin
from .models import Category, TrainingCategory


class ArticleCountWidget(AdminTextInputWidget):
    template_name = 'admin/article_count_popup.html'

    def __init__(self, private_count, public_count):
        super().__init__()
        self.private_count = private_count
        self.public_count = public_count

    def render(self, request, value=None, attrs=None):
        context = self.get_context(value, attrs)
        context.update({
            'total_count': value,
            'private_count': 10,
            'public_count': 25,
        })
        return mark_safe(render_to_string(self.template_name, context, request=request))


class CategoryAdmin(TreeAdmin, CustomizedFormFieldMixin, TranslationAdmin, MediaMixin):
    form = movenodeform_factory(Category)

    search_fields = ('name',)

    list_display = ('name', 'slug', 'article_count', 'is_active',)

    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": ("name_en",)}

    def article_count(self, obj):
        private_count = obj.private_article_count
        public_count = obj.public_article_count
        total_count = obj.article_count

        template = f"""
                <a tabindex="0" class="btn btn-md btn-danger" 
                    data-bs-trigger="hover focus"
                    role="button" data-bs-toggle="popover"
                    data-bs-trigger="focus" title="Article Count" 
                    data-bs-placement="top"
                    data-bs-content="Private Count : {private_count} &nbsp&nbsp  Public Count : {public_count}">{total_count}</a>
                """
        return mark_safe(template)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            article_count=Count("blogs"),
            private_article_count=Count("blogs", filter=Q(blogs__is_private=True)),
            public_article_count=Count("blogs", filter=Q(blogs__is_private=False)),
        )



admin.site.register(Category, CategoryAdmin)

