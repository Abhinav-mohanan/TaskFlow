import random
from django.core.mail import send_mail
from django.conf import settings
from .models import EmailOTP

def generate_and_save_otp(user):

    EmailOTP.objects.filter(user=user).delete()

    otp_code = random.randint(100000, 999999)

    EmailOTP.objects.create(user=user, otp=otp_code)
    return otp_code

def send_otp_mail(user, purpose):
    
    otp_code = generate_and_save_otp(user)
    email = user.email

    if purpose == "signup":
        subject = "Verify Your Account"
        message = f"Welcome!\nYour signup verification code is: {otp_code}. It expires in 5 minutes."
    elif purpose == "login":
        subject = "Your Login OTP"
        message = f"Your login code is: {otp_code}. It expires in 5 minutes.\nDo not share this code."
    else:
        subject = "Your OTP Code"
        message = f"Your code is: {otp_code}. It expires in 5 minutes."
    
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False
    )
        