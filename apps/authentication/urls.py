from django.urls import path
from .views import (SignupView, VerifySignupOTP, ResendOTPView)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('verify_signup_otp/', VerifySignupOTP.as_view(), name='verify_signup_otp'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend_otp')
    
]