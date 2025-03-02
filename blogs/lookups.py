from ajax_select import register, LookupChannel
from .models import Category, Tag


@register('category')
class CategoryLookup(LookupChannel):
    model = Category

    def get_query(self, q, request):
        return self.model.objects.filter(name__icontains=q).order_by('id')


@register('tags')
class TagsLookup(LookupChannel):
    model = Tag

    def get_query(self, q, request):
        return self.model.objects.filter(name__icontains=q).order_by('id')
