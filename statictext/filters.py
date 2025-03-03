import django_filters
from .models import FaqCategory, FAQ


class FaqFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category', method='filter_by_category')

    def filter_by_category(self, queryset, name, value):
        try:
            category = FaqCategory.objects.get(slug=value)
        except FaqCategory.DoesNotExist:
            return queryset.none()

        return queryset.filter(category=category, category__is_active=True)

    class Meta:
        model = FAQ
        fields = ['category']
