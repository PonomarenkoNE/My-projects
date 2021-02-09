from django.forms import ModelForm, EmailInput, PasswordInput, TextInput
from django.contrib.auth.models import User
from .models import City, Subscribe


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]
        widgets = {
            "username": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            "password": PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            })
        }


class RegForm(ModelForm):
    class Meta:
        model = User
        fields = ["email", "username", "password"]
        widgets = {
            "email": EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            "username": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            "password": PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            })
        }


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ["name"]


class SubForm(ModelForm):
    class Meta:
        model = Subscribe
        fields = ["notification_period"]
