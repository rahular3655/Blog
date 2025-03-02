import time

from defender import utils as defender_utils
from django.conf import settings
from django.contrib.auth import login
from django.core import signing
from django.core.signing import dumps
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext_lazy
from drf_spectacular.utils import extend_schema
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import exceptions, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import UserOTP, User, UserDevice
from accounts.serializers.users import RegisterSerializer, UserVerifyOTPSerializer, LoginSerializer, EmailValidationSerializer, \
    TwoFactorSetupSerializer, TwoFactorResponseSerializer, ConfirmTwoFactorSetupSerializer, VerifyTwoFactorSerializer, \
    ForgotPasswordEmailValidationSerializer, PasswordResetSerializer, Verify2faResponseSerializer, SoftDeleteSerializer, \
    Get2FAResponseSerializer, Disable2faResponseSerializer
from common.serializers import UserVerificationMessageSerializer, ResponseMessageSerializer
from common.tasks import send_email


@extend_schema(tags=["User Authentication"], summary="User signup", request=RegisterSerializer)
class UserSignUp(APIView):
    """
    For user signup.When a user signs up, a confirmation email is
    sent to the user's registered email address for verification
    """

    def post(self, request):
        serializer = RegisterSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Encrypt the user's email
        encrypted_email = dumps(user.email, salt=settings.SALT_ENCRYPTION_KEY)

        resp = UserVerificationMessageSerializer(
            instance=dict(
                detail=gettext_lazy("Successfully signed up, please check your email for OTP"),
                verification_id=encrypted_email
            )
        )

        return Response(resp.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["User Authentication"], summary="User verify api", request=UserVerifyOTPSerializer)
class UserAccountVerificationView(APIView):
    """
        This API verifies the user account. \n
        The verification key and otp must be passed in the request body.
    """

    def post(self, request):
        serializer = UserVerifyOTPSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(email=serializer.validated_data['key'])
            otp = UserOTP.objects.get(otp=serializer.validated_data['otp'], user=user)
            if user.is_active:
                otp.delete()
                raise exceptions.PermissionDenied(detail=gettext_lazy("Your account is already activate.Try to login"))

            user.is_active = True
            user.is_email_verified = True
            user.save()
            otp.delete()
            resp = ResponseMessageSerializer(instance=dict(detail=gettext_lazy("Your account has been verified.")))
            return Response(data=resp.data, status=status.HTTP_200_OK)

        except UserOTP.DoesNotExist:
            raise exceptions.PermissionDenied(
                detail=gettext_lazy("Invalid OTP, Please try again")
            )
        except User.DoesNotExist:
            raise exceptions.NotFound(
                detail=gettext_lazy("User not found,Try to signup")
            )


@extend_schema(tags=["User Authentication"], summary="User Login", request=LoginSerializer)
class LoginView(KnoxLoginView):
    """
        This API is used to login the user. \n
        The username and password must be passed in the request body.
    """
    permission_classes = (AllowAny,)

    def post(self, request, **kwargs):
        """
        Login the user.
        """
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        # defender_utils.reset_failed_attempts(request, 'login')

        if settings.DEVICE_LIMIT is not None and settings.DEVICE_LIMIT > 0:
            tokens = AuthToken.objects.filter(user=serializer.validated_data['user']).select_related('user')

            # to delete the expired tokens and corresponding devices of request user.
            if tokens is not None:
                for auth_token in tokens:
                    if auth_token.expiry is not None:
                        if auth_token.expiry < timezone.now():
                            auth_token.delete()

            if UserDevice.objects.filter(token__user=serializer.validated_data['user']).prefetch_related(
                    'auth_token').count() >= settings.DEVICE_LIMIT:
                raise exceptions.PermissionDenied(detail=gettext_lazy("Device limit reached."))

        token = AuthToken.objects.create(serializer.validated_data['user'])[1]

        login(request, serializer.validated_data['user'])

        if serializer.validated_data['user'].is_2fa_enabled:
            secret_key = settings.SECRET_KEY_FOR_2FA_TOKEN  # Get secrect key from settings.
            current_time = int(time.time())
            data_to_encrypt = {
                'value': token,
                'timestamp': current_time,
            }
            encrypted_token = signing.dumps(data_to_encrypt, key=secret_key)  # Encrypt the token for security purpose.
            data = {'token': encrypted_token, 'is_2fa_enabled': serializer.validated_data['user'].is_2fa_enabled}

        else:
            data = {'token': token, 'is_2fa_enabled': serializer.validated_data['user'].is_2fa_enabled}

        return Response(data, status=status.HTTP_200_OK)


@extend_schema(tags=["User Authentication"], summary="User verification resend email", request=EmailValidationSerializer)
class ResendOTPVerificationEmail(APIView):
    """
        This API resends the verification email to the user.
        The user email must be passed in the request body.
    """

    # throttle_classes = [CustomRequestThrottle]

    def post(self, request):
        """
        Sends a verification email to the user.
        """
        serializer = EmailValidationSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        encrypted_email = dumps(serializer.validated_data['email'], salt=settings.SALT_ENCRYPTION_KEY)
        otp = UserOTP.get_otp_by_email(serializer.validated_data['email'])
        message = render_to_string(
            template_name="email/signup.html",
            context=dict(
                subject="Please verify your email",
                user=otp.user.username,
                otp=otp.otp,
                domain=settings.BASE_DOMAIN,
            )
        )
        send_email.send(
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_email=str(otp.user.email),
            subject="Hello from Blogs.com. Please verify your email",
            message=message
        )

        resp = UserVerificationMessageSerializer(instance=dict(
            detail=gettext_lazy("OTP has been sent to your email, please check"),
            verification_id=encrypted_email))

        return Response(resp.data, status=status.HTTP_200_OK)


class Setup2FAView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["2FA-Authentication"], summary="Setup user 2-Factor Authentication.", responses=TwoFactorResponseSerializer)
    def get(self, request):
        """ 
        API to setup 2FA to a loggedIN user.
        """
        serializer = TwoFactorSetupSerializer(data={}, context={'request': request})
        serializer.is_valid(raise_exception=True)
        resp_serializer = TwoFactorResponseSerializer(instance=dict(
            qr_code=serializer.validated_data[0],
            uri=serializer.validated_data[1]
        ))
        return Response(data=resp_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(tags=["2FA-Authentication"], summary="Confirm after completing 2FA setup.", request=ConfirmTwoFactorSetupSerializer,
                   responses=ResponseMessageSerializer)
    def post(self, request):
        """ 
        API to Confirm 2FA is enabled by loggedIN user.
        """
        serializer = ConfirmTwoFactorSetupSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        resp_serializer = ResponseMessageSerializer(instance=dict(
            detail='2FA is successfully enabled.'
        ))
        return Response(data=resp_serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["2FA-Authentication"], summary="Verify 2FA.", request=VerifyTwoFactorSerializer,
               responses=Verify2faResponseSerializer)
class Verify2FAView(APIView):
    """ 
    API to Verify 2FA for a loggedIN user. \n
    An `Encrypted token` and `otp` are the inputs. \n
    Encrypted token is valid only for 3 min.
    """

    def post(self, request, *args, **kwargs):
        serializer = VerifyTwoFactorSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        resp_serializer = Verify2faResponseSerializer(instance=dict(
            detail='OTP verification successful.',
            token=serializer.validated_data
        ))
        return Response(data=resp_serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["2FA-Authentication"], summary="Get 2FA status.", responses=Get2FAResponseSerializer)
class Get2FAView(APIView):
    """ 
    API to get 2fa status of logged in user.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        resp_serializer = Get2FAResponseSerializer(instance=dict(
            is_2fa_enabled=request.user.is_2fa_enabled
        ))
        return Response(data=resp_serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["2FA-Authentication"], summary="Disable 2FA.", responses=Disable2faResponseSerializer)
class Disable2FAView(APIView):
    """ 
    API to Disable 2FA for a loggedIN user.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user
        user.is_2fa_enabled = False
        user.secret_2fa_key = None
        user.save()
        resp = Disable2faResponseSerializer(instance={"detail": gettext_lazy("Successfully disabled 2fa."),
                                                      "is_2fa_enabled": user.is_2fa_enabled
                                                      })
        return Response(data=resp.data, status=status.HTTP_200_OK)


@extend_schema(tags=["User Password"], summary="Send Email confirmation", request=ForgotPasswordEmailValidationSerializer)
class ForgotPasswordRequestView(APIView):
    """
    This API is used to reset the user's password.
    The user email must be passed in the request body in the first step.
    """

    def post(self, request):
        serializer = ForgotPasswordEmailValidationSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        encrypted_email = dumps(serializer.validated_data['email'], salt=settings.SALT_ENCRYPTION_KEY)
        otp = UserOTP.get_otp_by_email(serializer.validated_data['email'])
        message = render_to_string(
            template_name="email/forgot_password.html",
            context=dict(
                subject="Please verify your email",
                user=otp.user.username,
                otp=otp.otp,
                domain=settings.BASE_DOMAIN
            )
        )
        send_email.send(
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_email=str(otp.user.email),
            subject="Hello from Blogs.com. Please verify your email",
            message=message
        )

        resp = UserVerificationMessageSerializer(instance=dict(
            detail=gettext_lazy("otp has been sent to the your email account"),
            verification_id=encrypted_email))

        return Response(data=resp.data, status=status.HTTP_200_OK)


@extend_schema(tags=["User Password"], summary="Forgot password", request=PasswordResetSerializer)
class PasswordResetView(APIView):
    """
    Verify the key sent to the user's email and reset the user's password.
    """

    def post(self, request):
        """
        Verify the key sent to the user's email and reset the user's password.
        """
        serializer = PasswordResetSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        otp = UserOTP.objects.filter(user=serializer.validated_data['user'])
        otp.delete()
        resp = ResponseMessageSerializer(instance={"detail": gettext_lazy("Password updated successfully.")})
        return Response(data=resp.data, status=status.HTTP_200_OK)


@extend_schema(tags=["User - Account"], summary="Delete User Account", responses=ResponseMessageSerializer)
class AccountDeleteAPIView(APIView):
    """
    API to delete the account of loggedIN user (self deletion).
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def delete(self, request):
        serializer = SoftDeleteSerializer(request.user, data={'is_deleted': True})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        request.user.auth_token_set.all().delete()  # Singing out the user from all devices.
        resp_serializer = ResponseMessageSerializer(instance=dict(
            detail='User Account has been deleted successfully.'
        ))
        return Response(data=resp_serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["User Signout"], summary="signout loggedIN user", responses=ResponseMessageSerializer)
class UserSignoutAPIView(APIView):
    """ 
    API to signout the user from loggedIN device.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request._auth.delete()
        resp = ResponseMessageSerializer(instance={"detail": gettext_lazy("Signed out successfully.")})
        return Response(data=resp.data, status=status.HTTP_200_OK)


@extend_schema(tags=["User Signout"], summary="signout loggedIN user", responses=ResponseMessageSerializer)
class SignoutAllAPIView(APIView):
    '''
    API to signout the loggedIN user from all devices.
    '''
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        request.user.auth_token_set.all().delete()
        resp = ResponseMessageSerializer(instance={"detail": gettext_lazy("Successfully Signed out from all devices .")})
        return Response(data=resp.data, status=status.HTTP_200_OK)


def verify_email(request, slug):
    try:
        user = User.objects.get(slug=slug)
        user.is_email_verified = True
        user.save()
        # Redirect to the frontend URL after verification
        return redirect("https://Blogs.com-frontend.vercel.app/app")
    except User.DoesNotExist:
        return HttpResponse("User not found", status=404)
