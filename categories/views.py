from drf_spectacular.utils import extend_schema
from rest_framework.generics import RetrieveAPIView, ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response

from .models import Category
from .serializers import CategoryListSerializer


@extend_schema(tags=["categories"], summary="List all categories.", responses=CategoryListSerializer)
class CategoryList(ListAPIView):
    pagination_class = None
    queryset = Category.get_root_nodes()
    serializer_class = CategoryListSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


@extend_schema(tags=["categories"], summary="Category detail.", responses=CategoryListSerializer)
class CategoryDetails(RetrieveAPIView):
    serializer_class = CategoryListSerializer
    lookup_field = 'slug'
    queryset = Category.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class ListCategoryChildren(RetrieveAPIView):
    serializer_class = CategoryListSerializer
    lookup_field = 'slug'
    queryset = Category.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
