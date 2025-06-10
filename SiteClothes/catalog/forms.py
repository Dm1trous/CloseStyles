from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import PromoCode

class ApplyPromoCodeForm(forms.Form):
    promocode = forms.CharField(label='Промокод', required=False)

    def clean_promocode(self):
        data = self.cleaned_data['promocode'].strip()
        return data


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    password = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput,
    )
    error_messages = {
        'invalid_login': (
            "Неверное имя пользователя или пароль. "
            "Пожалуйста, проверьте введенные данные и попробуйте снова."
        ),
        'inactive': ("Эта учетная запись неактивна."),
    }
