from django.db import models
from django.urls import reverse
from django.utils.html import mark_safe
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from sorl.thumbnail.fields import ImageField
from django_lifecycle import hook, LifecycleModelMixin, AFTER_CREATE, AFTER_UPDATE, BEFORE_CREATE, BEFORE_UPDATE
from django.core.cache import cache
from django.test import RequestFactory
from django.urls import reverse
from django.utils.cache import get_cache_key

from accounts.models import User
from categories.models import Category
from tags.models import Tag
from .queryset import BlogQuerySet
from common.models import BaseImageModel


class Blog(LifecycleModelMixin,BaseImageModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_blogs")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="blogs")
    title = models.CharField(max_length=200, unique=True)
    short_description = models.TextField()
    content = models.TextField(_('Content'))
    featured_image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    alt_text = models.TextField(max_length=126, blank=True, null=True, help_text="Alt text field for featured image")
    featured = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    published_on = models.DateTimeField(null=True, blank=True)
    unpublished_on = models.DateTimeField(null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=False, null=True)
    is_draft = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, related_name='blogs', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    meta_title = models.TextField(blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keyword = models.TextField(blank=True, null=True)

    pass

    objects = BlogQuerySet.as_manager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_url(self):
        return reverse('blog_page', args=[self.category.slug, self.slug])
    
    @hook(AFTER_UPDATE)
    def invalidate_cache(self):
        cache_key = 'for_you_blogs_api_queryset'  # Cache key for for-you api
        cache.delete(cache_key)
        
    def __str__(self):
        return self.title


class BlogImage(BaseImageModel):
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    blog = models.ForeignKey(Blog, related_name='slideshow_images', on_delete=models.CASCADE)
    alt_text = models.TextField(max_length=126, blank=True, null=True)

    pass

    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="%s" width="100px" height="100px" />' % (self.image.url))
        else:
            return ""

    def __str__(self):
        return self.blog.title

    class Meta:
        ordering = ['display_order']


class BlogVideo(BaseImageModel):
    """This model used for add videos slideshows in blogs"""
    video = models.FileField(upload_to='blog_videos/', null=True, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    blog = models.ForeignKey(Blog, related_name='slideshow_videos', on_delete=models.CASCADE)
    thumbnail = ImageField(upload_to='blog_videos_thumbnail/', null=True, blank=True)
    alt_text = models.TextField(max_length=126, blank=True, null=True, help_text="Alt text field for video thumbnail image")

    pass

    def __str__(self):
        return self.blog.title

    class Meta:
        ordering = ['display_order']
