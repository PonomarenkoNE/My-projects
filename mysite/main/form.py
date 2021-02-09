from django.forms import ModelForm, EmailInput, PasswordInput, TextInput
from django.contrib.auth.models import User
from cloudinary.forms import CloudinaryFileField
from .models import Profile, Post



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


class ImgForm(ModelForm):
    avatar = CloudinaryFileField()
    class Meta:
        model = Profile
        fields = ["avatar"]


class PostForm(ModelForm):
    photo = CloudinaryFileField()
    class Meta:
        model = Post
        fields = ["text", "photo"]
