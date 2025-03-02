from django.conf import settings
from django.shortcuts import redirect, render
from django.utils.translation import get_language_info
from drf_spectacular.utils import extend_schema
from rest_framework import filters
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from blogs.models import Blog
from blogs.serializers import BlogListSerializer
from common.serializers import LanguageInfoSerializer


@extend_schema(tags=["Languages"], summary="List all Languages.", responses=LanguageInfoSerializer)
class LanguageListView(APIView):
    """ 
    API to get all languages used for multilingual functionalities.
    """

    def get(self, request):
        language_info_list = [get_language_info(lang[0]) for lang in settings.LANGUAGES]
        serializer = LanguageInfoSerializer(instance=language_info_list, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["Global Search"], summary="List Blogs based on search.", responses=BlogListSerializer)
class GlobalSearchViewAPI(ListAPIView):
    """ 
    API to get all articles based on search globally. \n
    Search supports `category`, `tags`, `title`, `descriptions`, `content` fields of the article.
    """
    serializer_class = BlogListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['category__name', 'category__description', 'title', 'short_description', 'tags__name', 'tags__description', 'content',
                     'meta_title', 'meta_description', 'meta_keyword']

    def get_queryset(self):
        return Blog.objects.prefetch_related(
            'user',
            'category',
            'tags',
            'user__profile'
        ).published()

