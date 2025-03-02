from django import forms
from django.contrib.auth.admin import UserChangeForm

from .models import User


class CustomUserChangeForm(UserChangeForm):
    send_email_button = forms.BooleanField(
        required=False,
        initial=False,
        label='Send Email Verification',
    )

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'is_email_verified', 'contact_number', 'last_login', 'is_superuser', 'groups', 'user_permissions', 'is_staff', 'date_joined', 'is_deleted', 
            'is_username_updated', 'is_author', 'is_instructor', 'is_active', 'preferred_language', 'is_2fa_enabled', 'secret_2fa_key', 'slug')

    def clean(self):
        cleaned_data = super().clean()
        send_email_button = cleaned_data.get('send_email_button')

        if send_email_button and self.instance.is_email_verified:
            raise forms.ValidationError("Email is already verified.")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the widget attributes based on the value of is_email_verified
        if self.instance.is_email_verified:
            self.fields['is_email_verified'].widget.attrs['checked'] = 'checked'

        if self.instance.is_email_verified:
            self.fields['email'].widget.attrs['readonly'] = True
