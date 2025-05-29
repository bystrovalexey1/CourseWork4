import os
import secrets

from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from dotenv import load_dotenv

from .forms import CustomUserCreationForm
from .models import CustomUser

load_dotenv(override=True)


class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/email-confirm/{token}'
        send_mail(
            subject='Добро пожаловать в интернет-магазин BystrovStore!',
            message = f'Спасибо, что зарегистрировались в нашем сервисе! Для подтверждения почты перейди по ссылке {url}',
            from_email=os.getenv('EMAIL_HOST_USER'),
            recipient_list=[user.email]
        )
        return super().form_valid(form)

def email_verification(request, token):
    user = get_object_or_404(CustomUser, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))