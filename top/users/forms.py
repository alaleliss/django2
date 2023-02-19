from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'label': 'Придумате никнейм'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'label': 'Придумайте пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'label': 'Повторите пароль'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class SignInForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'label': 'Напишите никнейм'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'label': 'Напишите пароль'}))

    class Meta:
        model = User
        fields = ['username', 'password']
