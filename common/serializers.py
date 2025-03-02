import os

from rest_framework import serializers
from sorl.thumbnail import get_thumbnail


class ResponseMessageSerializer(serializers.Serializer):
    detail = serializers.CharField()


class DeviceResponseMessageSerializer(serializers.Serializer):
    device_id = serializers.IntegerField()
    detail = serializers.CharField()


class UserVerificationMessageSerializer(serializers.Serializer):
    detail = serializers.CharField()
    verification_id = serializers.CharField()


class LanguageInfoSerializer(serializers.Serializer):
    code = serializers.CharField()
    name = serializers.CharField()
    name_local = serializers.CharField()
    name_translated = serializers.CharField()


class WebPImageUrlSerializer(serializers.Serializer):
    def to_representation(self, instance):
        if instance:
            req = self.context.get('request')
            path = instance.path

            original_width = instance.width
            original_height = instance.height
            if path and os.path.exists(path):
                if path.endswith('.webp'):
                    return req.build_absolute_uri(instance.url)
                else:
                    image = get_thumbnail(instance, f'{original_width}x{original_height}', format='WEBP', quality=75)
                    return req.build_absolute_uri(image.url)


class ImageSerializer(serializers.Serializer):
    xsmall = serializers.SerializerMethodField()
    medium = serializers.SerializerMethodField()
    large = serializers.SerializerMethodField()
    xlarge = serializers.SerializerMethodField()
    original = serializers.SerializerMethodField()

    def build_url(self, instance, size):
        req = self.context.get('request')
        path = instance.path
        if path and os.path.exists(path):
            image = get_thumbnail(instance, size, format='WEBP', quality=75)
            return req.build_absolute_uri(image.url)
        else:
            return None

    def get_xsmall(self, instance):
        return self.build_url(instance, size='100x100')

    def get_medium(self, instance):
        return self.build_url(instance, size='500x500')

    def get_large(self, instance):
        return self.build_url(instance, size='700x700')

    def get_xlarge(self, instance):
        return self.build_url(instance, size='1200x1200')

    def get_original(self, instance):
        req = self.context.get('request')
        path = instance.path
        original_width = instance.width
        original_height = instance.height
        if path and os.path.exists(path):
            if path.endswith('.webp'):
                return req.build_absolute_uri(instance.url)
            else:
                image = get_thumbnail(instance, f'{original_width}x{original_height}', format='WEBP', quality=75)
                return req.build_absolute_uri(image.url)
