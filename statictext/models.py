from django.db import models
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.


class StaticText(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:  # Only generate a new slug if it's not provided
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Static text"


class CompanyDetails(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    phone = PhoneNumberField(null=True, blank=True, unique=True)
    logo = models.ImageField(upload_to="company_logo/", null=True, blank=True)
    logo_white = models.ImageField(upload_to="company_logo/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Company setting'
        verbose_name_plural = "Company setting"


class SocialMediaUrl(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    image = models.ImageField(upload_to="social_media/", null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    company = models.ForeignKey(CompanyDetails, on_delete=models.CASCADE, related_name="urls")

    def __str__(self):
        return self.name


class Regulations(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, help_text="eg.setting_name")
    description = models.TextField(max_length=256, null=True, blank=True)
    value = models.TextField("value", null=True, blank=True)
    is_public = models.BooleanField(default=True, blank=True, help_text="Should this value be accessible to the public/users")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Regulations'
        verbose_name_plural = "Regulations"


class FaqCategory(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=False, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Faq Categories'


class FAQ(models.Model):
    category = models.ForeignKey(FaqCategory, on_delete=models.CASCADE, null=True, blank=True, related_name="faqs")
    question = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.question


class FAQAnswer(models.Model):
    question = models.ForeignKey(FAQ, on_delete=models.CASCADE, null=True, blank=True, related_name='faqs')
    answer = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class DropDownClass(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=False, null=True)
    is_active = True
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Drop Down'


class DropDown(models.Model):
    value = models.CharField(max_length=100, null=True, blank=True)
    drop_class = models.ForeignKey(DropDownClass, on_delete=models.CASCADE, null=True, blank=True, related_name="dropdowns")

    def __str__(self):
        return self.value
