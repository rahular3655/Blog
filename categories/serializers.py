from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from common.serializers import ImageSerializer
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'image', 'alt_text', 'description')

    @extend_schema_field(field=ImageSerializer)
    def get_image(self, obj):
        if obj.image:
            requests = self.context.get('request')
            if requests:
                return ImageSerializer(obj.image, context={'request': requests}).data
        return None


class CategoryReverseListSerializer(serializers.ModelSerializer):
    ancestor = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    @extend_schema_field(field='categories.serializers.CategoryReverseListSerializer')
    def get_ancestor(self, obj):
        parent = obj.get_parent()
        if not parent:
            return None
        return CategoryReverseListSerializer(instance=parent).data

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'image', 'alt_text', 'description', 'ancestor')

    @extend_schema_field(field=ImageSerializer)
    def get_image(self, obj):
        if obj.image:
            requests = self.context.get('request')
            if requests:
                return ImageSerializer(obj.image, context={'request': requests}).data
        return None


class CategoryListSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    # @extend_schema_field(field='categories.serializers.CategoryListSerializer')
    def get_children(self, obj):
        request = self.context['request']
        active_children = obj.get_children().filter(is_active=True)
        return CategoryListSerializer(instance=active_children, many=True, context={'request': request}).data

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'image', 'alt_text', 'description', 'children')

    @extend_schema_field(field=ImageSerializer)
    def get_image(self, obj):
        if obj.image:
            requests = self.context.get('request')
            if requests:
                return ImageSerializer(obj.image, context={'request': requests}).data
        return None
