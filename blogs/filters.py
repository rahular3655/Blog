import django_filters
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from django.contrib.admin import SimpleListFilter
from accounts.models import User
from categories.models import Category
from .models import Blog


class BlogFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(
        field_name='category',
        method='filter_by_category'
    )

    tags = django_filters.AllValuesMultipleFilter(
        field_name='tags__slug',
        method='filter_by_tags'
    )

    author = django_filters.CharFilter(
        field_name='author',
        method='filter_by_author'
    )

    def filter_by_category(self, queryset, name, value):
        try:
            category = Category.objects.get(slug=value)
        except Category.DoesNotExist:
            return queryset.none()

        q_objects = Q(category_id=category.pk) | Q(category__in=category.get_descendants())

        return queryset.filter(q_objects)

    def filter_by_tags(self, queryset, name, value):
        q_objects = Q(tags__slug__in=value)
        return queryset.filter(q_objects)

    def filter_by_author(self, queryset, name, value):
        try:
            author = User.objects.get(slug=value)
        except User.DoesNotExist:
            return queryset.none()

        return queryset.filter(user=author, user__is_author=True, user__is_active=True, user__is_deleted=False)

    class Meta:
        model = Blog
        fields = ['category', 'tags', 'featured', 'is_popular', 'author']


class CustomSearchFilter(SimpleListFilter):
    title = _('Search')  # Displayed title for the filter
    parameter_name = 'search'  # URL parameter for the filter

    def lookups(self, request, model_admin):
        return (
            ('contains', _('Contains')),  # Lookup option for 'contains' search
        )

    def queryset(self, request, queryset):
        if self.value() == 'contains':
            search_term = request.GET.get('q')  # Get the search term from query parameters
            if search_term:
                # Modify the queryset to filter based on the search term
                return queryset.filter(user__email__icontains=search_term)
        return queryset
