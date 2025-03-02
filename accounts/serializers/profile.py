from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.core import signing
from django.core.signing import loads
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions
from rest_framework import serializers

from accounts.models import User, UserProfile, SupportRequest, UserOTP, ContactInformation
from statictext.serializer import DropDownSerializer
from common.serializers import WebPImageUrlSerializer


class UserProfileSerializer(serializers.ModelSerializer):
    gender = DropDownSerializer()
    height_unit = DropDownSerializer()
    weight_unit = DropDownSerializer()

    profile_image = WebPImageUrlSerializer()

    class Meta:
        model = UserProfile
        fields = ['profile_image', 'gender', 'height', 'height_unit', 'weight', 'weight_unit', 'BMI', 'date_of_birth']


class UserDetailSerializer(serializers.ModelSerializer):
    """ 
    Serializer for  get details of `User`.
    """
    userprofile = UserProfileSerializer(source='profile')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'contact_number', 'is_instructor', 'userprofile', 'is_email_verified',
                  'is_contact_number_verified', 'is_active']
        read_only_fields = ['is_instructor']

    def to_representation(self, instance):
        serialized_data = super().to_representation(instance)

        if self.instance.contact_number:
            phone_number_country_code, phone_number_without_country_code = instance.get_country_code()
            serialized_data['phone_number_country_code'] = phone_number_country_code
            serialized_data['phone_number_without_country_code'] = phone_number_without_country_code

        return serialized_data


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """ 
    Serializer to update `user_profile` except `profile_image`.
    """

    class Meta:
        model = UserProfile
        fields = ['gender', 'height', 'height_unit', 'weight', 'weight_unit', 'date_of_birth']
        read_only_fields = ['BMI']


class UserUpdateSerializer(serializers.ModelSerializer):
    """ 
    Serializer to update user details.
    """
    profile = UserProfileUpdateSerializer()
    username = serializers.CharField(required=True, trim_whitespace=True)

    def validate_username(self, value):
        name = value.lower()
        request = self.context.get('request')
        user = request.user

        # username can be change only once, checking username is changed before.
        if user.is_username_updated:
            raise serializers.ValidationError(detail="Username cannot change again!")

        # Check if the new username is unique
        if User.objects.filter(username=name).exists():
            raise serializers.ValidationError(detail="Username exists! Please try another username!")
        return value

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        profile_instance = instance.profile
        for attr, value in profile_data.items():
            setattr(profile_instance, attr, value)

        profile_instance.save()
        instance.save()
        return instance


class EmailUpdateSerializer(serializers.Serializer):
    """ 
    Serializer to update user details.
    """
    email = serializers.EmailField(required=True, trim_whitespace=True)

    def validate_email(self, value):
        """
        Custom validation method to check if the email already exists.
        """
        email = value.lower()

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                detail=_("Email already exists.")
            )
        return email


class EmailVerifyOTPSerializer(serializers.Serializer):
    """
    Validating the key and OTP.
    """
    key = serializers.CharField(required=True)
    otp = serializers.CharField(required=True, max_length=6)

    def validate_key(self, value):
        """
        Returns the email.
        """
        try:
            decrypted = loads(value, salt=settings.SALT_ENCRYPTION_KEY, max_age=settings.ACCOUNT_VERIFICATION_AGE)
        except signing.SignatureExpired:
            raise exceptions.ValidationError(
                detail=_("Your OTP is expired please request another one")
            )
        except signing.BadSignature:
            raise exceptions.ValidationError(
                detail=_("Unable verify your account, please try again")
            )

        return decrypted


class ChangePasswordSerializer(serializers.Serializer):
    """ 
    Serializer to change password of a user.
    Validate Old password and new Password.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Invalid old password')
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance


class UserProfileImageSerializer(serializers.ModelSerializer):
    """ 
    Serializer for update `profile_image` of a user.
    """
    profile_image = serializers.ImageField()

    def validate_profile_image(self, value):
        # Validating image size is less than 5MB.
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("The picture size should be less than 5MB.")
        return value

    class Meta:
        model = UserProfile
        fields = ['profile_image']


class EmailUpdateSerializer(serializers.Serializer):
    """ 
    Serializer to update email.
    """
    email = serializers.EmailField(required=True, trim_whitespace=True)

    def validate_email(self, value):
        """
        Custom validation method to check if the email already exists.
        """
        email = value.lower()
        request = self.context['request']
        user = request.user

        if User.objects.filter(email=email).exists():
            raise exceptions.PermissionDenied(
                detail=_("Email already exists.")
            )
        user.change_email = None  # Set change email to None, for using this same api for resent OTP api.
        user.save()  # Otherwise email will not sent again for the same value in change_email field

        return email


class EmailVerifyOTPSerializer(serializers.Serializer):
    """
    Validating the key and OTP.
    """
    key = serializers.CharField(required=True)
    otp = serializers.CharField(required=True, max_length=6)

    def validate_key(self, value):
        """
        Returns the email.
        """
        try:
            decrypted = loads(value, salt=settings.SALT_ENCRYPTION_KEY, max_age=settings.ACCOUNT_VERIFICATION_AGE)
        except signing.SignatureExpired:
            raise exceptions.PermissionDenied(
                detail=_("Your OTP is expired please request another one !")
            )
        except signing.BadSignature:
            raise exceptions.PermissionDenied(
                detail=_("Unable to verify your account, please try again !")
            )

        return decrypted


class CreateSupportRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportRequest
        fields = ['title', 'message']

    def create(self, validated_data):
        user = self.context.get('request').user
        validated_data['user_id'] = user.id
        return super().create(validated_data)


class CreateContactInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInformation
        fields = ['first_name', 'last_name', 'title', 'email', 'message']


class SupportRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportRequest
        fields = ['user', 'title', 'message', 'created_at', 'status']


class ContactNumberUpdateSerializer(serializers.ModelSerializer):
    """ 
    Serializer to update contact number.
    """

    def validate(self, attrs):
        contact_number = attrs.get('change_contact_number')
        if User.objects.filter(contact_number=contact_number).exists():
            raise exceptions.PermissionDenied(_("This Contact Number already exist !"))
        return attrs

    class Meta:
        model = User
        fields = ['change_contact_number']

    def update(self, instance, validated_data):
        # Update the 'change_contact_number' field of the User instance
        instance.change_contact_number = validated_data.get('change_contact_number')
        instance.save()

        return instance


class ContactNumberVerifyOTPSerializer(serializers.Serializer):
    """
    Validating the OTP.
    """
    otp = serializers.CharField(required=True, max_length=6)

    def validate_otp(self, value):
        user = self.context.get('request').user

        try:
            otp = UserOTP.objects.get(otp=value, user=user)
        except:
            raise exceptions.PermissionDenied(_("OTP is invalid, please try again !"))

        time_difference = timezone.now() - otp.created_at

        if time_difference.total_seconds() > 300:  # 300 sec, the expiry time for otp is set to 5 min !
            otp.delete()
            raise exceptions.PermissionDenied(_("OTP is expired, please try again !"))
        user.contact_number = user.change_contact_number
        user.change_contact_number = None
        user.save()
        otp.delete()  # Deleting the OTP from UserOTP table.
        return True
