from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import CustomUser
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