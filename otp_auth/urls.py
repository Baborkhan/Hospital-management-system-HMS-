"""
MedFind OTP Auth — URL Configuration

Mount in main urls.py:
    path('api/v1/accounts/', include('otp_auth.urls')),
"""
from django.urls import path
from .views import SendOTPView, VerifyOTPView, ResendOTPView

urlpatterns = [
    # Point 5 — Send OTP
    path('send-otp/',    SendOTPView.as_view(),   name='otp-send'),
    # Point 6 — Verify OTP
    path('verify-otp/',  VerifyOTPView.as_view(),  name='otp-verify'),
    # Point 9 — Resend OTP (also aliased from frontend's old URL pattern)
    path('resend-otp/',  ResendOTPView.as_view(),  name='otp-resend'),

    # Legacy URL aliases used by existing login.html frontend:
    path('send-login-otp/',   SendOTPView.as_view(),   name='otp-send-legacy'),
    path('verify-login-otp/', VerifyOTPView.as_view(), name='otp-verify-legacy'),
]

