from django.conf import settings
from drf_spectacular.utils import extend_schema_field
from readtime import of_text
from rest_framework import serializers

from accounts.models import User
from accounts.serializers.users import UserSerializer
from categories.serializers import CategorySerializer, CategoryReverseListSerializer
from common.serializers import ImageSerializer
from tags.serializers import TagSerializer
from .models import Blog, BlogImage, BlogVideo
from common.serializers import WebPImageUrlSerializer


class BlogImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = BlogImage
        fields = ['image', 'alt_text', 'display_order']

    @extend_schema_field(field=ImageSerializer)
    def get_image(self, obj):
        requests = self.context['request']
        return ImageSerializer(obj.image, context={'request': requests}).data


class BlogVideoSerializer(serializers.ModelSerializer):
    video = serializers.SerializerMethodField

    thumbnail = WebPImageUrlSerializer()

    class Meta:
        model = BlogVideo
        fields = ['video', 'thumbnail', 'alt_text', 'display_order']


class CategoryWithParentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class BlogListSerializer(serializers.ModelSerializer):
    author = UserSerializer(source='user')
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    read_time = serializers.SerializerMethodField()  # Custom field for read time
    breadcrumbs = serializers.SerializerMethodField()
    featured_image = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            'id', 'slug', 'author', 'category', 'breadcrumbs', 'title', 'short_description', 'tags', 'featured', 'is_popular', 'is_private',
            'published_on',
            'featured_image', 'alt_text', 'read_time', 'meta_title', 'meta_description', 'meta_keyword',
        ]

    @extend_schema_field(field=CategoryReverseListSerializer)
    def get_breadcrumbs(self, obj):
        return CategoryReverseListSerializer(obj.category).data

    def get_read_time(self, obj):
        content = obj.content
        read_time = of_text(content, wpm=settings.BLOG_READ_TIME_WPM).text  # Calculate read time using the readtime package
        return read_time

    @extend_schema_field(field=ImageSerializer)
    def get_featured_image(self, obj):
        requests = self.context['request']
        if obj.featured_image:
            return ImageSerializer(obj.featured_image, context={'request': requests}).data
        else:
            return None


class ForYouBlogListSerializer(serializers.Serializer):
    slug = serializers.SlugField()
    title = serializers.CharField()
    blogs = BlogListSerializer(many=True)


class BlogDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(source='user')
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    read_time = serializers.SerializerMethodField()  # Custom field for read time
    breadcrumbs = serializers.SerializerMethodField()  # Custom field for category's ancestors
    slideshow_images = BlogImageSerializer(many=True)
    slideshow_videos = BlogVideoSerializer(many=True)
    featured_image = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            'author', 'category', 'breadcrumbs', 'title', 'short_description', 'content', 'slideshow_images', 'slideshow_videos', 'tags',
            'featured', 'is_popular', 'is_published', 'is_private', 'published_on', 'featured_image', 'read_time', 'meta_title', 'meta_description',
            'meta_keyword',
        ]
        read_only_fields = ('id', 'slug', 'created_at', 'updated_at',)

    @extend_schema_field(field=CategoryReverseListSerializer)
    def get_breadcrumbs(self, obj):
        return CategoryReverseListSerializer(obj.category).data

    def get_read_time(self, obj):
        content = obj.content
        read_time = of_text(content, wpm=settings.BLOG_READ_TIME_WPM).text  # Calculate read time using the readtime package
        return read_time

    def to_representation(self, instance):
        user = self.context['user']

        if not user and instance.is_private:
            raise serializers.ValidationError("Permission denied, Need to be logged in to view this blog.")

        representation = super().to_representation(instance)
        return representation

    @extend_schema_field(field=ImageSerializer)
    def get_featured_image(self, obj):
        requests = self.context['request']
        if obj.featured_image:
            return ImageSerializer(obj.featured_image, context={'request': requests}).data
        else:
            return None


class RelatedBlogListSerializer(serializers.ModelSerializer):
    read_time = serializers.SerializerMethodField()  # Custom field for read time
    featured_image = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            'id', 'slug', 'title', 'short_description', 'featured_image', 'is_private', 'read_time', 'created_at', 'published_on', 'meta_title',
            'meta_description', 'meta_keyword',
        ]

    def get_read_time(self, obj):
        content = obj.content
        read_time = of_text(content, wpm=settings.BLOG_READ_TIME_WPM).text  # Calculate read time using the readtime package
        return read_time

    @extend_schema_field(field=ImageSerializer)
    def get_featured_image(self, obj):
        requests = self.context['request']
        if obj.featured_image:
            return ImageSerializer(obj.featured_image, context={'request': requests}).data
        else:
            return None


class AuthorsListSerializer(serializers.ModelSerializer):
    blog_count = serializers.IntegerField()
    profile_image = serializers.ImageField(source='profile.profile_image')

    class Meta:
        model = User
        fields = ['id', 'slug', 'first_name', 'last_name', 'blog_count', 'profile_image']


class AuthorDetailSerializer(serializers.ModelSerializer):
    blog_count = serializers.IntegerField()
    profile_image = serializers.ImageField(source='profile.profile_image')

    class Meta:
        model = User
        fields = ['id', 'slug', 'first_name', 'last_name', 'blog_count', 'profile_image']
