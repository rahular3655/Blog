from django.utils.translation import gettext_lazy
from knox.models import AuthToken
from knox.settings import CONSTANTS
from rest_framework import serializers, exceptions
from django.conf import settings

from accounts.models import UserDevice


class UserDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDevice
        fields = ['id', 'device_type', 'access_type', 'device_brand', 'device_model', 'app_version', 'device_os', 'ip_address', 'browser']


class UpdateUserDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDevice
        fields = ['device_type', 'access_type', 'device_brand', 'device_model', 'app_version', 'device_os', 'ip_address', 'browser']

    def validate(self, attrs):
        request = self.context['request']

        if settings.DEVICE_LIMIT is not None and settings.DEVICE_LIMIT > 0:
            if UserDevice.objects.filter(token__user=request.user).count() >= settings.DEVICE_LIMIT:
                raise exceptions.PermissionDenied(detail=gettext_lazy("Device limit reached."))

        if attrs.get('access_type') == 'app':
            required_fields = ['device_type', 'access_type', 'device_brand', 'device_model', 'app_version', 'device_os', 'ip_address']
            for field in required_fields:
                if not attrs.get(field):
                    raise serializers.ValidationError(f"{field} is required.")

        elif attrs.get('access_type') == 'web':
            required_fields = ['device_type', 'access_type', 'browser', 'ip_address']
            for field in required_fields:
                if not attrs.get(field):
                    raise serializers.ValidationError(f"{field} is required.")

        return attrs

    def create(self, validated_data):
        request = self.context['request']
        auth_header = request.headers.get('Authorization')
        token_key = auth_header.split()[1]
        token = AuthToken.objects.filter(token_key=token_key[:CONSTANTS.TOKEN_KEY_LENGTH]).first()
        if token:
            if UserDevice.objects.filter(token=token).exists():
                raise serializers.ValidationError("A device with this token already exists")
        return UserDevice.objects.create(token=token, **validated_data)
