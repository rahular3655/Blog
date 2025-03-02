from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from knox.auth import TokenAuthentication
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import UserDevice
from accounts.serializers.device import UserDeviceSerializer, UpdateUserDeviceSerializer
from common.serializers import ResponseMessageSerializer, DeviceResponseMessageSerializer


@extend_schema(tags=["User - Devices"], summary="Add user-device details", request=UserDeviceSerializer,
               responses=DeviceResponseMessageSerializer)
class CreateUserDeviceView(APIView):
    """ 
    API to create the device details of loggedIN user.
    
    - `device_type` should be --> 
            `pc`, `phone` or `tablet`.
            
     - `access_type` should be --> 
            `web` or `app`.
    
    Need to pass the device details in request --> 
    
        if access_type == "app" (loggedIN from mobile),  
            the required field are = ['device_type', 'access_type', 'device_brand', 'device_model', 'app_version', 'device_os', 'ip_address']
    
        if access_type == "web" (loggedIN from browser),
            the required field are = ['device_type', 'access_type', 'browser','ip_address']
            
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UpdateUserDeviceSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        resp_serializer = DeviceResponseMessageSerializer(instance=dict(
            device_id=instance.id,
            detail=_('User Device has been created successfully.')
        ))
        return Response(data=resp_serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["User - Devices"], summary="Get User devices Details", responses=UserDeviceSerializer)
class UserDeviceListAPIView(APIView):
    """
    API to get all the devices that user currently loggedIN.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_devices = UserDevice.objects.filter(token__user_id=request.user)
        device_details = [user_device.get_device_details_dict() for user_device in user_devices]
        serialized_data = UserDeviceSerializer(device_details, many=True)
        return Response(data=serialized_data.data, status=status.HTTP_200_OK)


@extend_schema(tags=["User - Devices"], summary="Signout account from a device", responses=ResponseMessageSerializer)
class UserDeviceSignOutAPIView(APIView):
    """ 
    API to signout a specific device that the request.user is loggedIN.
    Pass the user_device_id in url.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, user_device_id):
        user_device = get_object_or_404(UserDevice, id=user_device_id)  # fetching the userdevice
        auth_token = user_device.token  # fetch token from user_device
        if auth_token.user == request.user:  # validating token is corresponding to requesting user.
            auth_token.delete()  # deleting token and signout device.
            user_device.delete()
            resp_serializer = ResponseMessageSerializer(instance=dict(
                detail=_("Successfully signout user from device.")
            ))
            return Response(data=resp_serializer.data, status=status.HTTP_200_OK)
        raise PermissionDenied(
            detail=_("You do not have permission to perform this action.")
        )
