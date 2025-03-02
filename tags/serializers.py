from rest_framework import serializers

from .models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'description', 'slug']


class TagListSerializer(serializers.ModelSerializer):
    blog_count = serializers.IntegerField()

    class Meta:
        model = Tag
        fields = ['id', 'name', 'description', 'slug', 'blog_count']
