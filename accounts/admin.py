from django.contrib import admin
from django.db import models
from django.db.models import Manager
from django.utils.html import format_html

from common.utils import CustomizedFormFieldMixin
from .form import CustomUserChangeForm
from .models import User, UserProfile, UserOTP, UserDevice, SupportRequest, ContactInformation


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    extra = 0
    can_delete = False

    def get_queryset(self, request):
        qs = super().get_queryset(request=request)
        return qs.prefetch_related('user')


class UserDeviceInline(admin.TabularInline):
    model = UserDevice
    extra = 0
    can_delete = False

    def get_queryset(self, request):
        qs = super().get_queryset(request=request)
        return qs.prefetch_related('user')


class UserOTPInline(admin.StackedInline):
    model = UserOTP
    extra = 0
    can_delete = False

    def get_queryset(self, request):
        qs = super().get_queryset(request=request)
        return qs.prefetch_related('user')


class NonDeletedUserAdminMixin:
    "Mixin to display only non deleted users in all models user dropdown in admin panel.(is_deleted = False)"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user' or db_field.name == 'author' and issubclass(db_field.related_model, models.Model):
            kwargs['queryset'] = db_field.related_model.objects.filter(is_deleted=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class NonDeletedAuthorsAdminMixin:
    "Mixin to display only non deleted authors in all blog user dropdown in admin panel.(is_deleted = False, is_author=True)"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user' or db_field.name == 'author' and issubclass(db_field.related_model, models.Model):
            kwargs['queryset'] = db_field.related_model.objects.filter(is_deleted=False, is_author=True, is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class UserModelAdmin(NonDeletedUserAdminMixin, CustomizedFormFieldMixin, admin.ModelAdmin):
    form = CustomUserChangeForm

    list_display = ['username', 'email', 'verified', 'is_active', 'is_author', 'is_deleted', ]

    exclude = ('password', 'change_email', 'change_contact_number',)

    inlines = [UserProfileInline, UserOTPInline, UserDeviceInline]

    search_fields = ('username', 'first_name', 'email',)

    list_filter = ('is_active', 'is_author', 'is_deleted', 'is_instructor',)

    prepopulated_fields = {'slug': ('username',)}

    fieldsets = (
        # Add the custom fieldset for the send email button
        ('User Details', {
            'fields': ('username', 'first_name', 'last_name', 'email', 'send_email_button', 'is_email_verified', 'contact_number',
                       'last_login', 'is_superuser', 'groups', 'user_permissions', 'is_staff', 'date_joined',
                       'is_deleted', 'is_username_updated', 'is_author', 'is_instructor', 'is_active', 'preferred_language',
                       'is_2fa_enabled', 'secret_2fa_key', 'slug')
        }),
    )

    def get_queryset(self, request):
        # Override the default queryset to show only non-deleted users
        return super().get_queryset(request).prefetch_related('auth_token_set').filter(is_deleted=False)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Customize the user dropdowns to only display non-deleted users
        if db_field.name == 'user':
            kwargs['queryset'] = User.objects.filter(is_deleted=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def verified(self, obj):
        if not obj.is_email_verified:
            return format_html('<span style="color: red;">Not Verified</span>')
        return format_html('<span style="color: green;">Verified &#10003;</span>')

    verified.short_description = "Email Status"
    verified.allow_tags = True

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if form.cleaned_data.get('send_email_button'):
            User.send_verification_link(obj)


class SupportRequestAdmin(CustomizedFormFieldMixin, admin.ModelAdmin):
    list_display = ('user', 'title', 'status',)


class ContactInformationAdmin(CustomizedFormFieldMixin, admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'title', 'email', 'status',)


class UserDeviceAdmin(CustomizedFormFieldMixin, admin.ModelAdmin):
    list_display = ('username', 'user', 'device_type', 'ip_address',)
    list_filter = ('device_type',)

    def get_queryset(self, request):
        qs = super().get_queryset(request=request)
        return qs.prefetch_related('token__user')

    def username(self, obj):
        return obj.token.user

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class FilteredAuthorManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_author=True)


class AuthorModelAdmin(NonDeletedUserAdminMixin, CustomizedFormFieldMixin, admin.ModelAdmin):
    list_display = ['username', 'email', 'is_active', 'is_author', 'is_deleted', 'blogs_count', 'courses_count', 'classes_count']

    exclude = (
        'password', 'last_login', 'is_superuser', 'groups', 'user_permissions', 'is_staff', 'date_joined', 'change_email', 'change_contact_number',)

    readonly_fields = ('blogs_count', 'courses_count', 'classes_count',)

    search_fields = ('username', 'first_name', 'email',)

    list_filter = ('is_active', 'is_author', 'is_deleted', 'is_instructor',)

    prepopulated_fields = {'slug': ('username',)}

    def get_queryset(self, request):
        # Override the default queryset to show only non-deleted users
        return super().get_queryset(request).filter(is_deleted=False)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Customize the user dropdowns to only display non-deleted users
        if db_field.name == 'user':
            kwargs['queryset'] = User.objects.filter(is_deleted=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class AuthorModel(User):
    objects = FilteredAuthorManager()

    class Meta:
        verbose_name = 'Author List'
        verbose_name_plural = 'Authors List'
        proxy = True


admin.site.register(AuthorModel, AuthorModelAdmin)
admin.site.register(User, UserModelAdmin)
admin.site.register(ContactInformation, ContactInformationAdmin)
admin.site.register(UserDevice, UserDeviceAdmin)
admin.site.register(SupportRequest, SupportRequestAdmin)
