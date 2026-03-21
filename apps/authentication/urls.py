from django.urls import path
from .views import (SignupView, VerifySignupOTP, ResendOTPView, LoginView,
                    VerifyLoginOTPView, HomeView)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('verify_signup_otp/', VerifySignupOTP.as_view(), name='verify_signup_otp'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend_otp'),
    path('', LoginView.as_view(), name='login'),
    path('verify_login_otp', VerifyLoginOTPView.as_view(), name='verify_login_otp'),
    path('home', HomeView.as_view(), name='home'),

    
]