from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput, FileInput, EmailInput

from .models import Profile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'last_name',
            'email',
            'first_name'
        ]

        widgets = {
            "email": EmailInput(attrs={
                'class': 'div-profil-form-element-input3',
                'placeholder': 'Новая электронная почта',
            }),
            "last_name": TextInput(attrs={
                'class': 'div-profil-form-element-input3',
                'placeholder': 'Введите вашу фамилию',
            }),
            "first_name": TextInput(attrs={
                'class': 'div-profil-form-element-input3',
                'placeholder': 'Введите ваше имя'
            }),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'image'
        ]

        widgets = {
            "image": FileInput(attrs={
                'class': 'div-profil-form-element-input4',
                'accept': '.jpeg,.png, .jpg, .webp'
            }),
        }


