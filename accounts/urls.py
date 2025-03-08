from django.urls import path

from accounts.views import auth, users, user_device

app_name = "accounts"

urlpatterns = [

    # Auth
    path('signup/', auth.UserSignUp.as_view(), name='user_signup'),
    path('verify-user-account/', auth.UserAccountVerificationView.as_view(), name='verify_user_account'),
    path('login/', auth.LoginView.as_view(), name='login_user'),
    path('resend-verification-otp/', auth.ResendOTPVerificationEmail.as_view(), name='resend_verification_otp'),
    path('request-reset-password/', auth.ForgotPasswordRequestView.as_view(), name='request_reset_password'),
    path('reset-password/', auth.PasswordResetView.as_view(), name='reset_password'),

    # # 2FA
    # path('get-2fa/', auth.Get2FAView.as_view(), name='get-2fa'),
    # path('setup-2fa/', auth.Setup2FAView.as_view(), name='setup-2fa'),
    # path('verify-2fa/', auth.Verify2FAView.as_view(), name='verify-2fa'),
    # path('disable-2fa/', auth.Disable2FAView.as_view(), name='disable-2fa'),

    # User Profile
    path('get-profile/', users.UserProfileDetailAPIView.as_view(), name='get_profile'),
    path('update-profile/', users.UserProfileUpdateView.as_view(), name='update_profile'),
    path('update-profile-image/', users.UserProfileImageUpdateView.as_view(), name='update_profile_image'),
    path('change-password/', users.ChangePasswordView.as_view(), name='change_password'),

    path('update-email/', users.UpdateEmailAPIView.as_view(), name='update_email'),
    path('verify-email/', users.EmailVerificationView.as_view(), name='verify_email'),

    path('update-contact-number/', users.UpdateContactNumberAPIView.as_view(), name='update_contact_number'),
    path('verify-contact-number/', users.ContactNumberVerificationView.as_view(), name='verify_contact_number'),

    # Support
    path('support-requests/all/', users.SupportRequestAPIView.as_view(), name='get-all-support-requests'),
    path('support-request/create/', users.CreateSupportRequestAPIView.as_view(), name='create-support-request'),

    # Contact Informations
    path('contact-information/create/', users.CreateContactInformationAPIView.as_view(), name="create-contact-information"),

    # User Device
    path('add_device_details/', user_device.CreateUserDeviceView.as_view(), name='add_device_details'),
    path('get_device_details/', user_device.UserDeviceListAPIView.as_view(), name='device_details'),
    path('signout_device/<int:user_device_id>/', user_device.UserDeviceSignOutAPIView.as_view(), name='signout_device'),

    # User Signout
    path('signout/', auth.UserSignoutAPIView.as_view(), name='user_signout'),
    path('signout-all/', auth.SignoutAllAPIView.as_view(), name='signout_all'),

    # Account Delete
    path('delete/', auth.AccountDeleteAPIView.as_view(), name='account-delete'),

    # verify email from admin panel
    path('verify-email/<slug:slug>/', auth.verify_email, name='verify_email'),

]
