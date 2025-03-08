import base64
import io
import random
import string

import pyotp
import qrcode
from defender import utils as defender_utils
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.core import signing
from django.core.signing import loads
from django.utils.translation import gettext_lazy
from knox.auth import TokenAuthentication
from rest_framework import exceptions
from rest_framework import serializers

from accounts.models import User, UserProfile, UserOTP

from rest_framework.exceptions import AuthenticationFailed
import os


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for `profile_image` of user.
    Used in Blogs.
    """

    class Meta:
        model = UserProfile
        fields = ['profile_image']


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for `User` Model.
    Used in Blogs and Video stream.
    """

    userprofile = UserProfileSerializer(source='profile')

    class Meta:
        model = User
        fields = ['id', 'slug', 'first_name', 'last_name', 'email', 'username', 'is_instructor', 'userprofile']


class User2faSerializer(serializers.ModelSerializer):
    """
    Serializer for 2factor authentication.
    """

    class Meta:
        model = User
        fields = ['secrect_key_2fa']


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    re_enter_password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        the password is strong enough.
        """
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        re_enter_password = data.get('re_enter_password')

        if User.objects.filter(username=username).exists():
            raise exceptions.PermissionDenied(
                gettext_lazy("Username exists!. Please try another username!")
            )

        if User.objects.filter(email=email).exists():
            raise exceptions.PermissionDenied(
                gettext_lazy("Email already exists.Try to login")
            )

        if password != re_enter_password:
            raise exceptions.PermissionDenied(gettext_lazy('Passwords do not match.Please check'))

        return data

    def create(self, validated_data):
        """
        Create and return a new User instance.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )

        User.send_verification_email(user)
        return user


class UserVerifyOTPSerializer(serializers.Serializer):
    """
        Validating the key and otp
    """
    key = serializers.CharField(required=True)
    otp = serializers.CharField(required=True, max_length=6)

    def validate_key(self, value):
        """
        Returns the email
        """
        try:
            decrypted = loads(value, salt=settings.SALT_ENCRYPTION_KEY, max_age=settings.ACCOUNT_VERIFICATION_AGE)
        except signing.SignatureExpired:
            raise exceptions.ValidationError(
                detail=gettext_lazy("Your OTP is expired please request another one")
            )
        except signing.BadSignature:
            raise exceptions.ValidationError(
                detail=gettext_lazy("Unable verify your account, please try again")
            )

        return decrypted


class LoginSerializer(serializers.Serializer):
    """Validating user with username/email and password"""

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if defender_utils.is_already_locked(request=self.context.get('request'), username=username):
            raise exceptions.PermissionDenied(detail=gettext_lazy(
                "Your account is blocked due to too many failed login attempts. Please try again later."),
                code='account_blocked')

        user = authenticate(username=username, password=password)

        if not user:
            """
            Checking the user is already block or not.And if there is too many
            attempts the user will be blocked using django defender
            """
            defender_utils.record_failed_attempt(defender_utils.get_ip(self.context.get('request')), username)

            raise exceptions.AuthenticationFailed(detail=gettext_lazy('Invalid Credentials'))

        if user.is_deleted:
            raise exceptions.PermissionDenied(detail=gettext_lazy("Invalid Credentials."))

        if not user.is_active:
            raise exceptions.PermissionDenied(detail=gettext_lazy("Your account is not activated."), code='account_inactive')

        if not user.is_email_verified:
            raise exceptions.PermissionDenied(detail=gettext_lazy("Your account is not activated."), code='account_inactive')

        attrs['user'] = user
        return attrs


class EmailValidationSerializer(serializers.Serializer):
    """
    Validates the email address.

    The email address must exist and must not be already verified.
    """
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        user = get_user_model().objects.filter(email=value).first()
        if not user:
            raise serializers.ValidationError(gettext_lazy("No account. Try to sign up."))
        if user.is_email_verified:
            raise serializers.ValidationError(gettext_lazy("Your account is already verified."))
        if user.is_active:
            raise serializers.ValidationError(gettext_lazy("Your account is already verified."))
        if defender_utils.is_user_already_locked(user.username):
            raise serializers.ValidationError(gettext_lazy("Your account is blocked. Try again later."))
        return value

    def create(self, validated_data):
        user = get_user_model().objects.get(email=validated_data['email'])

        try:
            user_otp = UserOTP.objects.get(user=user)
            user_otp.delete()
        except UserOTP.DoesNotExist:
            pass  # No existing OTP to remove

        user_otp = UserOTP.objects.create(user=user)

        return user_otp


class TwoFactorSetupSerializer(serializers.Serializer):

    def validate(self, validated_data):
        request = self.context['request']
        user = request.user

        # Check if 2FA is already enabled for the user
        if user.is_2fa_enabled:
            raise exceptions.PermissionDenied(detail=gettext_lazy('2FA is already enabled for this account.'))

        # Generate a secret key for 2FA
        secret_key = pyotp.random_base32()

        # Set the secret key for the user
        user.secret_2fa_key = secret_key
        user.save()

        # Construct the provisioning URI.
        # OTP digit count is default to 6 digits.
        # The time period for which each OTP is valid is default to 30 seconds.
        uri = pyotp.totp.TOTP(secret_key).provisioning_uri(
            name=user.email,
            issuer_name="kalpafit",
        )

        # Generate the QR code.
        qr = qrcode.QRCode(
            version=1,  # You can adjust the version as needed.
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,  # Adjust the box size as needed.
            border=4,  # Adjust the border as needed.
        )
        qr.add_data(uri)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")  # Create a QR code image.
        stream = io.BytesIO()
        img.save(stream, "PNG")
        data_uri = f"data:image/png;base64,{base64.b64encode(stream.getvalue()).decode('utf-8')}"

        return [data_uri, uri]


class TwoFactorResponseSerializer(serializers.Serializer):
    """ 
    Serializer to give response for 2FA setup.
    """
    qr_code = serializers.URLField()
    uri = serializers.CharField()


class ConfirmTwoFactorSetupSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6, required=True)

    def validate_otp(self, value):
        if not value.isdigit():
            raise exceptions.ValidationError(detail=gettext_lazy("OTP must consist of numeric digits."))
        return value

    def validate(self, attrs):
        request = self.context['request']
        user = request.user
        otp = attrs.get("otp")

        if user.is_2fa_enabled:
            raise exceptions.PermissionDenied(detail=gettext_lazy("2FA is already enabled for this account."))

        totp = pyotp.TOTP(user.secret_2fa_key)  # Verify the provided OTP code

        if totp.verify(otp):
            user.is_2fa_enabled = True  # 2FA setup is confirmed; mark it as enabled in the database
            user.save()
            return True
        else:
            raise exceptions.PermissionDenied(detail=gettext_lazy("Invalid OTP code. 2FA setup is incomplete."))


class VerifyTwoFactorSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6, required=True)
    encrypted_token = serializers.CharField(required=True)  # Encrypted token that send from login api is return here for validation.

    def validate_otp(self, value):
        if not value.isdigit():
            raise exceptions.ValidationError(detail=gettext_lazy("OTP must consist of numeric digits."))
        return value

    def validate_encrypted_token(self, value):
        try:
            data = signing.loads(value, key=settings.SECRET_KEY_FOR_2FA_TOKEN,
                                 max_age=180)  # 3min is set as maximum time period to decrypt the token.
            return data.get('value')
        except signing.SignatureExpired:
            raise exceptions.PermissionDenied(gettext_lazy("Unable to login, please try again."))
        except signing.BadSignature:
            raise exceptions.PermissionDenied(gettext_lazy("Unable to login, please try again."))

    def validate(self, attrs):
        token = attrs.get('encrypted_token')
        token_bytes = token.encode('utf-8')
        user, auth_token = TokenAuthentication().authenticate_credentials(token_bytes)
        otp = attrs.get("otp")

        if not user.is_2fa_enabled:
            raise exceptions.ValidationError(detail=gettext_lazy("2FA is not enabled for this account."))

        totp = pyotp.TOTP(user.secret_2fa_key)  # Verify the provided OTP code

        if totp.verify(otp):
            return token
        else:
            raise exceptions.PermissionDenied("Invalid OTP code.")


class Verify2faResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()
    token = serializers.CharField()


class Disable2faResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()
    is_2fa_enabled = serializers.BooleanField()


class Get2FAResponseSerializer(serializers.Serializer):
    is_2fa_enabled = serializers.BooleanField()


class ForgotPasswordEmailValidationSerializer(serializers.Serializer):
    """
    Email validation serializer
    """
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        user = User.objects.filter(email=value).first()
        if not user:
            raise serializers.ValidationError(
                gettext_lazy("We couldn't find an account with that email address. Please check your email and try again."))

        if not user.is_email_verified:
            raise serializers.ValidationError(gettext_lazy("Your account is not verified.Please verify your account"))

        if not user.is_active:
            raise serializers.ValidationError(gettext_lazy("Your account is not verified.Please verify your account"))

        if defender_utils.is_already_locked(request=self.context.get('request'), username=user.username):
            raise serializers.ValidationError(gettext_lazy("Your account is blocked. Try again later."))

        return value

    def create(self, validated_data):
        user = get_user_model().objects.get(email=validated_data['email'])

        try:
            user_otp = UserOTP.objects.get(user=user)
            user_otp.delete()
        except UserOTP.DoesNotExist:
            pass  # No existing OTP to remove

        user_otp = UserOTP.objects.create(user=user)

        return user_otp


class PasswordResetSerializer(serializers.Serializer):
    key = serializers.CharField(write_only=True, required=True)
    otp = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    reentered_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        """
        Custom validation method to check if the new_password and reentered_password fields match.
        """
        key = data.get('key')
        otp = data.get('otp')
        new_password = data.get('new_password')
        reentered_password = data.get('reentered_password')

        try:
            email = loads(key, salt=settings.SALT_ENCRYPTION_KEY, max_age=settings.PASSWORD_RESET_AGE)

        except signing.SignatureExpired:
            errors = {'key': gettext_lazy('Your OTP is expired please request another one')}
            raise exceptions.ValidationError(errors)
        except signing.BadSignature:
            errors = {'key': gettext_lazy('Unable verify your account, please try again')}
            raise exceptions.ValidationError(errors)

        user = User.objects.get(email=email)

        if not UserOTP.objects.filter(user=user, otp=otp).exists():
            raise exceptions.NotFound(detail=gettext_lazy('OTP not found, Try again later'))

        if new_password != reentered_password:
            errors = {'password': gettext_lazy('Passwords do not match.')}
            raise exceptions.ValidationError(errors)

        data['user'] = user
        return data

    def save(self, **kwargs):
        new_password = self.validated_data['new_password']
        user = self.validated_data['user']
        user.set_password(new_password)
        user.save()


class SoftDeleteSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['is_deleted', 'email', 'contact_number']

    def update(self, instance, validated_data):
        if instance.is_deleted:
            raise serializers.ValidationError('User Account already deleted.')

        # Generate a random email
        random_email = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) + '@invalid.com'

        # Update the instance fields
        instance.email = random_email
        instance.contact_number = None
        instance.is_deleted = True
        instance.is_active = False
        instance.save()

        return instance
