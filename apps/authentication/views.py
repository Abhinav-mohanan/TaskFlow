from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.views import View
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .models import CustomUser, EmailOTP
from .forms import SignupForm
from .utils import send_otp_mail


class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'authentication/signup.html'
    success_url = reverse_lazy('verify_signup_otp')

    def form_valid(self, form):
        user = form.save()

        send_otp_mail(user=user, purpose='signup')
        self.request.session['signup_email'] = user.email
        
        return super().form_valid(form)


class VerifySignupOTP(View):
    def get(self, request):
        email = request.session.get('signup_email')

        if not email:
            return redirect('signup')
        
        context = {
            'email': email,
            'title': 'Verify Your Account',
            'message': f"We sent a OTP to {email}.",
            'post_url': 'verify_signup_otp',
        }
        return render(request, 'authentication/verify_otp.html', context)
    
    def post(self, request):
        email = request.session.get('signup_email')
        entered_otp = request.POST.get('otp')

        if not email or not entered_otp:
            return redirect('signup')
        
        try:
            user = CustomUser.objects.get(email=email)
            otp_record = EmailOTP.objects.get(user=user)
            
            if str(otp_record.otp) == entered_otp:

                if otp_record.is_expired():
                    messages.error(request, "This code has expired. Please request a new one.")
                    return redirect('verify_signup_otp')

                user.is_active = True
                user.save()
                otp_record.delete()

                login(request, user)
                del request.session['signup_email']
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid OTP code. Please try again.")
                return redirect('verify_signup_otp')
            
        except (CustomUser.DoesNotExist, EmailOTP.DoesNotExist):
            messages.error(request, "An error occurred. Please try again.")
            return redirect('signup')

class ResendOTPView(View):
    def post(self, request):
        email = request.session.get('signup_email')
        
        if not email:
            email = request.session.get('login_email')
            purpose = 'login'
        else:
            purpose = 'signup'
        
        if not email:
            messages.error(request, "An error occurred. Please try again.")
            return redirect('login')
        
        try:
            user = CustomUser.objects.get(email=email)
            send_otp_mail(user, purpose)

            messages.success(request, f"A new OTP has been sent to {email}.")

            if purpose == 'signup':
                return redirect('verify_signup_otp')
            else:
                return redirect('verify_login_otp')
        
        except CustomUser.DoesNotExist:
            messages.error(request, "User not found. Please try again.")
            return redirect('signup')



class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        email = request.POST.get('username')
        password = request.POST.get('password')
        action = request.POST.get('action')

        if not email:
            messages.error(request, "Please enter your email address.")
            return redirect('login')
        
        try:
            user = CustomUser.objects.get(email=email)

            if not user.is_active:
                send_otp_mail(user, purpose='signup')
                request.session['signup_email'] = user.email
                messages.warning(request, "Please verify your account first. We've sent a code to your email.")
                return redirect('verify_signup_otp')
            
            if action == 'otp':
                send_otp_mail(user, purpose='login')
                request.session['login_email'] = user.email
                messages.success(request, "A login code has been sent to your email.")
                return redirect('verify_login_otp')
            
            elif action == 'password':
                if not password:
                    messages.error(request, "Please enter your password")
                    return redirect('login')
                
                auth_user = authenticate(request, email=email, password=password)

                if auth_user is not None:
                    login(request, auth_user)
                    return redirect('dashboard')
                else:
                    messages.error( request, "Incorrect password. Please try again.")
                    return redirect('login')
            else:
                messages.error(request, "Invalid request. Please try again.")
                return redirect('login')
                
        except CustomUser.DoesNotExist:
            messages.error(request, "Invalid credentials or account does not exist.")
            return redirect('login')


class VerifyLoginOTPView(View):

    def get(self, request):
        email = request.session.get('login_email')

        if not email:
            return redirect('login')
        
        context = {
            'email': email,
            'title': 'Login to Your Account',
            'message': f"We sent a OTP to {email}.",
            'post_url': 'verify_login_otp',
        }
        return render(request, 'authentication/verify_otp.html', context)
    
    def post(self, request):
        email = request.session.get('login_email')
        entered_otp = request.POST.get('otp')

        if not email:
            return redirect('login')

        try:
            user = CustomUser.objects.get(email=email)
            otp_record = EmailOTP.objects.get(user=user)

            if str(otp_record.otp) == entered_otp:
                if otp_record.is_expired():
                    messages.error(request, "OTP expiry please request a new one")
                    return redirect('verify_login_otp')
                if not user.is_active:
                        user.is_active = True
                        user.save()
                otp_record.delete()
                del request.session['login_email']
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid OTP")
                return redirect('verify_login_otp')

        except (CustomUser.DoesNotExist, EmailOTP.DoesNotExist):
            messages.error(request, "An error occurred. Please try again.")
            return redirect('signup')


class LogoutView(LoginRequiredMixin, View):
    def post(self, request):
        logout(request)
        messages.success(request, "Logged out successfully")
        return redirect('login')

                
                


                
            
            