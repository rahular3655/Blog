from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Tag
from .serializers import TagListSerializer


@extend_schema(tags=["Tags"], summary="List all tags.", responses=TagListSerializer)
class ListAllTagsAPIView(ListAPIView):
    """
    API to list all tags
    """
    queryset = Tag.objects.annotate_live_blog_count().all()
    serializer_class = TagListSerializer


@extend_schema(tags=["Tags"], summary="Tag details.", responses=TagListSerializer)
class TagDetailAPIView(RetrieveAPIView):
    """
    API to get details of a Tag.
    """
    serializer_class = TagListSerializer
    lookup_field = 'slug'
    queryset = Tag.objects.annotate_live_blog_count().all()
