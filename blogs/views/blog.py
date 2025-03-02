from django.db import models
from django.db.models import Case, When
from django.db.models import Value
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.pagination import PageNumberPagination
from rest_framework import exceptions
from rest_framework import filters
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.db.models import Q
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from accounts.models import User
from blogs.filters import BlogFilter
from blogs.models import Blog
from blogs.serializers import BlogListSerializer, BlogDetailSerializer, RelatedBlogListSerializer, AuthorsListSerializer, AuthorDetailSerializer, \
    ForYouBlogListSerializer
from categories.models import Category


@extend_schema(tags=["Blogs"], summary="List all Blogs.", responses=BlogListSerializer)
class ListAllBlogsAPIView(ListAPIView):
    """ 
    API to list all blogs.  \n
    Search supports `title` field of the article.  \n
    Ordering supports `created_at`,`published_on`,`featured`,`is_popular` - use field-name for ascending order and -field-name for descending order. \n
    By default the articles are in descending order based on the  `published_on` date.  \n 
    """
    current_datetime = timezone.now()
    serializer_class = BlogListSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = BlogFilter
    search_fields = ['title']
    ordering_fields = ['created_at', 'published_on', 'featured', 'is_popular']
    ordering = ['-published_on']
    
    # @method_decorator(cache_page(60 * 60))  # Cache for 15 minutes
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)

    
    def get_queryset(self):
        return Blog.objects.prefetch_related(
            'user',
            'category',
            'tags',
            'user__profile'
        ).published()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    
class OneCategoryPerPagePagination(PageNumberPagination):
    page_size = 2
    

@extend_schema(tags=["Blogs"], summary="For You.", responses=ForYouBlogListSerializer)
class ListForYouBlogsAPIView(ListAPIView):
    serializer_class = ForYouBlogListSerializer
    pagination_class = OneCategoryPerPagePagination

    def get_queryset(self):
        accept_lang = self.request.META.get('HTTP_ACCEPT_LANGUAGE')[:2]
        
        queryset = []
        if accept_lang != 'en':
            queryset = []
        else:
            cache.get('for_you_blogs_api_queryset')
    
        if queryset == []:
            second_level_categories = Category.objects.filter(depth=2)
            queryset = []
            for category in second_level_categories:
                blogs = Blog.objects.prefetch_related(
                        'user',
                        'category',
                        'tags',
                        'user__profile'
                    ).published().filter(Q(category = category) | Q(category__in=category.get_descendants())).order_by('?')[:9] 
                category_data = {
                    'slug': category.slug,
                    'title': category.name,
                    'blogs': blogs
                }
                queryset.append(category_data)
            cache.set('for_you_blogs_api_queryset', queryset, timeout=180)  # Cache for 3 min
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    

@extend_schema(tags=["Blogs"], summary="Blog details.", responses=BlogDetailSerializer)
class BlogDetailAPIView(RetrieveAPIView):
    """
    API to get selected blogs in detail.
    """
    serializer_class = BlogDetailSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Blog.objects.prefetch_related(
            'user',
            'category',
            'tags',
            'user__profile'
            ).published()

    def get_serializer_context(self):
        # Add request user in serialiser context
        context = super().get_serializer_context()
        context['user'] = self.request.user
        context['request'] = self.request
        return context


@extend_schema(tags=["Blogs"], summary="List related Blogs.", responses=RelatedBlogListSerializer)
class ListRelatedBlogsAPIView(ListAPIView):
    """ 
    API to list all related blogs  with respect to category of a given blog id.
    """
    serializer_class = RelatedBlogListSerializer
    pagination_class = None

    def get_queryset(self):
        blog_slug = self.kwargs.get('slug')

        try:
            blog = Blog.objects.published().filter(slug=blog_slug).prefetch_related('category').get()
        except Blog.DoesNotExist:
            raise exceptions.NotFound()

        category_id = [blog.category_id]
        siblings = [cat.id for cat in blog.category.get_siblings()]
        ancestors = [cat.id for cat in blog.category.get_ancestors()]
        all_others = list(Category.objects.exclude(pk__in=category_id + siblings + ancestors).values_list('pk', flat=True).all())

        return Blog.objects.published().filter(category_id__in=category_id + siblings + ancestors + all_others, is_draft=False, user__is_deleted=False).annotate(
            order_value=Case(
                When(category_id__in=category_id, then=Value(0)),
                When(category_id__in=siblings, then=Value(1)),
                When(category_id__in=ancestors, then=Value(2)),
                When(category_id__in=all_others, then=Value(3)),
                default=Value(4),
                output_field=models.PositiveSmallIntegerField()
            )
        ).order_by('order_value').all().exclude(slug=blog_slug)[:10]


@extend_schema(tags=["authors"], summary="List all Authors.", responses=AuthorsListSerializer)
class ListAllAuthorsAPIView(ListAPIView):
    filter_backends = [filters.SearchFilter]
    filterset_class = BlogFilter
    search_fields = ['first_name', 'last_name', 'username']
    serializer_class = AuthorsListSerializer
    current_datetime = timezone.now()
    queryset = User.user_objects.filter(is_author=True, is_active=True, is_deleted=False).prefetch_related('profile').annotate_live_blog_count()


@extend_schema(tags=["authors"], summary="Authors details.", responses=AuthorDetailSerializer)
class AuthorsDetailAPIView(RetrieveAPIView):
    serializer_class = AuthorDetailSerializer
    lookup_field = 'slug'
    queryset = User.user_objects.filter(is_author=True, is_active=True, is_deleted=False).annotate_live_blog_count().prefetch_related('profile').all()
