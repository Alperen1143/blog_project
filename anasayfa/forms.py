from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


class RegisterForm(forms.Form):
    full_name = forms.CharField(
        max_length=100,
        required=True,
        label="Ad Soyad"
    )

    username = forms.CharField(
        max_length=150,
        required=True,
        label="Kullanıcı Adı"
    )

    email = forms.EmailField(
        required=True,
        label="E-posta"
    )

    phone = forms.CharField(
        max_length=10,
        required=True,
        label="Telefon Numarası"
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput,
        label="Şifre"
    )

    password_confirm = forms.CharField(
        required=True,
        widget=forms.PasswordInput,
        label="Şifre Tekrar"
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if User.objects.filter(username=username).exists():
            raise ValidationError("Bu kullanıcı adı zaten kullanılıyor.")

        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise ValidationError("Bu e-posta adresi zaten kullanılıyor.")

        return email

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")

        if not phone.isdigit():
            raise ValidationError("Telefon numarası sadece rakamlardan oluşmalıdır.")

        if len(phone) != 10:
            raise ValidationError("Telefon numarası başında 0 olmadan 10 haneli olmalıdır.")

        return phone

    def clean_password(self):
        password = self.cleaned_data.get("password")

        if len(password) < 8:
            raise ValidationError("Şifre en az 8 karakter olmalıdır.")

        if not re.search(r"[A-Z]", password):
            raise ValidationError("Şifre en az bir büyük harf içermelidir.")

        if not re.search(r"[a-z]", password):
            raise ValidationError("Şifre en az bir küçük harf içermelidir.")

        if not re.search(r"[0-9]", password):
            raise ValidationError("Şifre en az bir rakam içermelidir.")

        return password

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise ValidationError("Şifreler eşleşmiyor.")

        return cleaned_data


class LoginForm(forms.Form):
    username_or_email = forms.CharField(
        max_length=150,
        required=True,
        label="Kullanıcı Adı veya E-posta"
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput,
        label="Şifre"
    )