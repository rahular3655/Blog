from datetime import datetime

from django.test import TestCase
from rest_framework import status

from accounts.models import User
from .models import Blog, Category, Tag


class BlogModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser1', password='testpassword')
        self.category = Category.objects.create(name='Test Category1')
        self.tag1 = Tag.objects.create(name='Tag3')
        self.tag2 = Tag.objects.create(name='Tag4')
        self.blog = Blog.objects.create(
            user=self.user,
            category=self.category,
            title='Test Blog Title',
            short_description='Short description',
            content='Blog content',
            image=None,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            featured=True,
            is_popular=False,
            is_published=True,
            published_on=datetime.now(),
            slug=None,
        )
        self.blog.tags.add(self.tag1, self.tag2)

    def test_retrieve_blog_list(self):
        response = self.client.get('/blogs/blogs/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_single_blog(self):
        blog = Blog.objects.create(**self.blog)
        response = self.client.get(f'/blogs/{blog.slug}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_blog(self):
        blog = Blog.objects.create(**self.blog_data)
        updated_data = {
            "title": "Updated Blog Title",
            "content": "Updated content",
        }
        response = self.client.patch(f'/api/blogs/{blog.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_blog(self):
        blog = Blog.objects.create(**self.blog_data)
        response = self.client.delete(f'/api/blogs/{blog.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
