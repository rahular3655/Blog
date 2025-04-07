import phonenumbers
from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django_lifecycle import hook, LifecycleModelMixin, AFTER_CREATE, AFTER_UPDATE, BEFORE_CREATE, BEFORE_UPDATE
from knox.models import AuthToken
from phonenumber_field.modelfields import PhoneNumberField
from sorl.thumbnail import get_thumbnail
from sorl.thumbnail.fields import ImageField

from common.models import BaseImageModel
# from common.tasks import send_email
from common.utils import random_file_name
from statictext.models import DropDown
from .queryset import UserQuerySet
from .utils import randint


class DevicesChoices(models.TextChoices):
    pc = ('pc', 'pc')
    phone = ('phone', 'phone')
    tablet = ('tablet', 'tablet')


class AccessChoices(models.TextChoices):
    web = ('web', 'web')
    app = ('app', 'app')


class StatusChoices(models.TextChoices):
    open = ('open', 'open')
    in_progress = ('in_progress', 'in progress')
    resolved = ('resolved', 'resolved')


class User(LifecycleModelMixin, AbstractUser):
    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False)
    change_email = models.EmailField(null=True, blank=True)
    contact_number = PhoneNumberField(null=True, blank=True, unique=True)
    is_contact_number_verified = models.BooleanField(default=False)
    change_contact_number = PhoneNumberField(null=True, blank=True, unique=True)
    is_deleted = models.BooleanField(default=False)
    is_username_updated = models.BooleanField(default=False)
    is_author = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    preferred_language = models.CharField(max_length=10, blank=True, choices=settings.LANGUAGES, default="en")
    is_2fa_enabled = models.BooleanField(default=False)
    secret_2fa_key = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=False, null=True)
    objects = UserManager()

    user_objects = UserQuerySet.as_manager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super().save(*args, **kwargs)

    @hook(BEFORE_CREATE, when='is_superuser', is_not=False)
    def set_superuser_active(self):
        self.is_active = True

    @hook(AFTER_CREATE, when_any=['is_superuser', 'is_staff'], is_now=False, priority=1)
    def create_user_otp(self):
        UserOTP.objects.create(user=self, created_at=timezone.now())

    @hook(AFTER_CREATE, when_any=['is_superuser', 'is_staff'], is_now=False, priority=2)
    def create_profile(self):
        UserProfile.objects.create(user=self)

    @hook(BEFORE_UPDATE, when='username', has_changed=True, is_not=None)
    def update_is_username_updated(self):
        self.is_username_updated = True

    @hook(AFTER_UPDATE, when='change_contact_number', has_changed=True, is_not=None)
    def create_contact_otp(self):
        UserOTP.objects.update_or_create(user=self, defaults={'user': self, 'otp': randint(), 'created_at': timezone.now()})
        
    @hook(BEFORE_UPDATE, when='contact_number', has_changed=True, is_not=None)
    def update_is_contact_number_verified(self):
        self.is_contact_number_verified = True

   

    def generate_verification_url(self):
        verification_path = reverse('accounts:verify_email', kwargs={'slug': self.slug})
        return f"{settings.BASE_DOMAIN}{verification_path}"

   

    def get_country_code(self):
        # Parse the phone number
        parsed_number = phonenumbers.parse(str(self.contact_number), None)

        # Get the country code in the format +xx
        country_code = "+{}".format(parsed_number.country_code)

        phone_number_without_country_code = phonenumbers.national_significant_number(parsed_number)

        return country_code, phone_number_without_country_code

    def blogs_count(self):
        return self.user_blogs.count()

    def classes_count(self):
        return self.user_classes.count()

    def courses_count(self):
        return self.user_courses.count()


class UserOTP(LifecycleModelMixin, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='otp')
    otp = models.PositiveIntegerField(default=randint)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email}'

    @staticmethod
    def get_otp_by_email(email_address: str):
        """Returns the UserOTP instance for the given email address."""
        otp = UserOTP.objects.filter(user__email=email_address).first()
        return otp

    @staticmethod
    def generate_or_replace_otp(user):
        # Check if an OTP already exists for the user     
        UserOTP.objects.update_or_create(user=user, defaults={'user': user, 'otp': randint(), 'created_at': timezone.now()})

    @staticmethod
    def get_otp(user: object):
        user_otp, created = UserOTP.objects.get_or_create(user=user)

        if not created:
            # If OTP already exists, update it with a new value
            user_otp.otp = randint()
            user_otp.created_at = timezone.now()
            user_otp.save()

        return user_otp.otp


class UserProfile(LifecycleModelMixin, BaseImageModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        help_text="One user is relate only with one profile."
    )

    gender = models.ForeignKey(DropDown, on_delete=models.CASCADE, blank=True, null=True, related_name="gender",
                               limit_choices_to={'drop_class__slug': 'gender'})
    profile_image = ImageField(upload_to=random_file_name, blank=True, null=True)
    height = models.FloatField(max_length=100, null=True, blank=True)
    height_unit = models.ForeignKey(DropDown, on_delete=models.CASCADE, null=True, blank=True, related_name="height_unit",
                                    limit_choices_to={'drop_class__slug': 'height-unit'})
    weight = models.FloatField(max_length=100, null=True, blank=True)
    weight_unit = models.ForeignKey(DropDown, on_delete=models.CASCADE, null=True, blank=True, related_name="weight_unit",
                                    limit_choices_to={'drop_class__slug': 'weight-unit'})
    BMI = models.FloatField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    pass

    @property
    def thumbnail(self):
        if self.profile_image:
            return get_thumbnail(self.profile_image, '200x20', quality=90)
        return None

    @hook(BEFORE_UPDATE, when_any=['height', 'weight', 'height_unit', 'weight_unit'], is_not=None)
    def calculate_bmi(self):
        if self.height and self.weight is not None:
            if self.height_unit.value.lower() == "inch":
                height_meter = self.height * 0.0254
            elif self.height_unit.value.lower() == "centimeter":
                height_meter = self.height / 100
            if self.weight_unit.value.lower() == "pound":
                weight_kg = self.weight * 0.453592
            elif self.weight_unit.value.lower() == "kilogram":
                weight_kg = self.weight
            self.BMI = round(weight_kg / (height_meter * height_meter), 2)

    def __str__(self):
        return self.user.email


class SupportRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="support",
                             help_text="One user can have multiple support requests."
                             )
    title = models.TextField()
    message = models.TextField()
    status = models.CharField(max_length=100, choices=StatusChoices.choices, default=StatusChoices.open)
    comments = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email


class UserDevice(LifecycleModelMixin, models.Model):
    # token = models.OneToOneField(AuthToken, on_delete=models.CASCADE, related_name="auth_token")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_device", null=True)
    device_type = models.CharField(max_length=100, choices=DevicesChoices.choices)
    access_type = models.CharField(max_length=100, choices=AccessChoices.choices)
    device_brand = models.CharField(max_length=100, null=True, blank=True)
    device_model = models.CharField(max_length=100, null=True, blank=True)
    app_version = models.CharField(max_length=100, null=True, blank=True)
    browser = models.CharField(max_length=100, null=True, blank=True)
    device_os = models.CharField(max_length=100, null=True)
    ip_address = models.GenericIPAddressField()

    def get_device_details_dict(self):
        if self.access_type == 'app':
            return {
                'id': self.id,
                'device_type': self.device_type,
                'access_type': self.access_type,
                'device_brand': self.device_brand,
                'device_model': self.device_model,
                'app_version': self.app_version,
                'device_os': self.device_os,
                'ip_address': self.ip_address
            }
        else:
            return {
                'id': self.id,
                'device_type': self.device_type,
                'access_type': self.access_type,
                'browser': self.browser,
                'ip_address': self.ip_address
            }

    @hook(AFTER_CREATE)
    def save_user(self):
        self.user = self.token.user
        self.save()

    def __str__(self):
        return f'{self.token.user}'


class ContactInformation(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=100, choices=StatusChoices.choices, default=StatusChoices.open)
    comments = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name_plural = "Contact Log"
