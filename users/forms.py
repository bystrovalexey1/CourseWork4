from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=35, required=True)
    usable_password = None

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "username",
            "phone_number",
            "avatar",
            "country",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите ваш email"}
        )
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите ваш логин"}
        )
        self.fields["phone_number"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите ваш номер телефона"}
        )
        self.fields["avatar"].widget.attrs.update(
            {
                "class": "form-control",
            }
        )
        self.fields["country"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите вашу страну"}
        )
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите ваш пароль"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Повторите ваш пароль"}
        )

    def cleane_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError("Введите верный номер телефона")
