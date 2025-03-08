from django.conf import settings
from django.core.signing import dumps
from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from knox.auth import TokenAuthentication
from rest_framework import filters
from rest_framework import status, exceptions
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, ListAPIView,GenericAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from accounts.models import SupportRequest
from accounts.models import User, UserProfile, UserOTP
from accounts.serializers.profile import UserDetailSerializer, UserUpdateSerializer, UserProfileImageSerializer, \
    ChangePasswordSerializer, EmailUpdateSerializer, EmailVerifyOTPSerializer, ContactNumberUpdateSerializer, \
    ContactNumberVerifyOTPSerializer, CreateSupportRequestSerializer, SupportRequestSerializer, CreateContactInformationSerializer
from common.serializers import ResponseMessageSerializer, UserVerificationMessageSerializer


@extend_schema(tags=["User - Profile"], summary="User Profile details.", responses=UserDetailSerializer)
class UserProfileDetailAPIView(RetrieveAPIView):
    """ 
    API to get  profile details of logged IN user.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer
    queryset = User.objects.prefetch_related('profile')

    def get_object(self):
        return self.request.user


@extend_schema(tags=["User - Profile"], summary="User profile partial update", methods=['PATCH'], request=UserUpdateSerializer,
               responses=ResponseMessageSerializer)
@extend_schema(methods=['PUT'], exclude=True)  # To remove PUT method from UpdateAPIView in swagger.
class UserProfileUpdateView(UpdateAPIView):
    """
    API to update Profile of loggedIN user. \n
    Need to pass ids in unit fields.
    Get the ids of "height unit", "weight unit" and "gender" from  \n
    /config/dropdown/list/ Api. \n
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer

    def get_object(self):
        return self.request.user

    def patch(self, request, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        resp_serializer = ResponseMessageSerializer(instance=dict(
            detail='Profile has been updated successfully.'
        ))
        return Response(data=resp_serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["User - Profile"], summary="Change Password", request=ChangePasswordSerializer,
               responses=ResponseMessageSerializer)
class ChangePasswordView(APIView):
    """
    API to change the password of loggedIN user. \n
    By entering `old_password` and `new_password`. \n
    The `new_password` need to satisfy : \n
           - Minimum Length should be 8 \n
           - Passwords to contain a mix of characters, such as uppercase letters, lowercase letters, numbers, and special characters. \n
           - Require at least one numeric character in the password. \n
           - Require at least one uppercase letter in the password. \n
           - Require at least one lowercase letter in the password. \n
           - Require at least one special character (e.g., !, @, #, $, %, etc.) in the password. \n
           - Should not be a Dictionary Words. \n
           - Password does not contain the user's username or any part of it. \n
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.update(request.user, serializer.validated_data)
        resp_serializer = ResponseMessageSerializer(instance=dict(
            detail='Password has been updated successfully.'
        ))
        return Response(data=resp_serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["User - Profile"], summary="User profile picture update", methods=['PUT'], request=UserProfileImageSerializer,
               responses=ResponseMessageSerializer)
@extend_schema(methods=['PATCH'], exclude=True)  # To remove PUT method from UpdateAPIView in swagger.
class UserProfileImageUpdateView(UpdateAPIView):
    """
    API to update Profile picture of loggedIN user.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileImageSerializer
    parser_classes = [MultiPartParser]

    def get_object(self):
        userprofile = UserProfile.objects.get(user=self.request.user)
        return userprofile

    def put(self, request):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        resp_serializer = ResponseMessageSerializer(instance=dict(
            detail='Profile Picture has been updated successfully.'
        ))
        return Response(data=resp_serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["User - Profile"], summary="Update Email", request=EmailUpdateSerializer)
class UpdateEmailAPIView(APIView):
    """ 
    API to update `email` of loggedIN user. \n
    A confirmation email with OTP is sent to the new email address for verification.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_scope = 'update-email'
    throttle_classes = [ScopedRateThrottle]

    def post(self, request):
        user = request.user
        serializer = EmailUpdateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        # Creating an OTP for the user.
        UserOTP.generate_or_replace_otp(user)

        # Adding new email to `change_email` field for future reference.
        user.change_email = serializer.validated_data['email']
        user.save()

        # Encrypt the user's email
        encrypted_email = dumps(serializer.validated_data['email'], salt=settings.SALT_ENCRYPTION_KEY)

        resp = UserVerificationMessageSerializer(
            instance=dict(
                detail=_("Please check your email for an OTP"),
                verification_id=encrypted_email
            )
        )
        return Response(resp.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["User - Profile"], summary="Email Verification", request=EmailVerifyOTPSerializer)
class EmailVerificationView(APIView):
    """
    This API verifies the email.
    The verification key and otp must be passed in the request body.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = EmailVerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            otp = UserOTP.objects.get(otp=serializer.validated_data['otp'], user=user)
            user.email = user.change_email  # Replacing old email with verified new email.
            user.change_email = None  # Set `change_email` to None.
            user.save()
            otp.delete()  # Deleting the OTP from UserOTP table.
            resp = ResponseMessageSerializer(instance=dict(detail=_("Successfully changed your email ! ")))
            return Response(data=resp.data, status=status.HTTP_200_OK)

        except UserOTP.DoesNotExist:
            raise exceptions.PermissionDenied(
                detail=_("Invalid OTP, Please try again")
            )


class CreateContactInformationAPIView(APIView):
    """ 
    API to create contact information.
    """

    @extend_schema(tags=["Contact - Informations"], summary="Create contact information", request=CreateContactInformationSerializer,
                   responses=ResponseMessageSerializer)
    def post(self, request):
        serializer = CreateContactInformationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        resp_serializer = ResponseMessageSerializer(instance=dict(
            detail="Contact Information is added successfully."
        ))
        return Response(data=resp_serializer.data, status=status.HTTP_200_OK)


class CreateSupportRequestAPIView(APIView):
    """
    API to create support requests for loggedIN user.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @extend_schema(tags=["User - Support"], summary="Create Support Request", request=CreateSupportRequestSerializer,
                   responses=ResponseMessageSerializer)
    def post(self, request):
        serializer = CreateSupportRequestSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        resp_serializer = ResponseMessageSerializer(instance=dict(
            detail='Support request created successfully.'
        ))
        return Response(data=resp_serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["User - Support"], summary="Get all Support Request", responses=SupportRequestSerializer)
class SupportRequestAPIView(ListAPIView):
    """ 
    API to get all support requests.                    
    """
    queryset = SupportRequest.objects.all()
    serializer_class = SupportRequestSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['user']
    search_fields = ['title', 'message']


@extend_schema(tags=["User - Profile"], summary="Update Contact Number", request=ContactNumberUpdateSerializer)
@extend_schema(methods=['PATCH'], exclude=True)  # To remove PUT method from UpdateAPIView in swagger.
class UpdateContactNumberAPIView(UpdateAPIView):
    """ 
    API to update `contact_number` of loggedIN user. \n
    An OTP is sent to the new Contact Number for verification. \n
    OTP will be valid only for 5min.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = ContactNumberUpdateSerializer

    def get_object(self):
        return self.request.user

    def put(self, request):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        resp_serializer = ResponseMessageSerializer(instance=dict(
            detail=_("Please check your phone for an OTP")
        ))
        return Response(data=resp_serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["User - Profile"], summary="Contact number Verification", request=ContactNumberVerifyOTPSerializer)
class ContactNumberVerificationView(APIView):
    """
    This API verifies the email. \n
    The verification key and otp must be passed in the request body. \n
    OTP is valid only for 5min.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ContactNumberVerifyOTPSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        resp_serializer = ResponseMessageSerializer(instance=dict(
            detail=_("Successfully changed your contact number !")
        ))
        return Response(data=resp_serializer.data, status=status.HTTP_200_OK)


