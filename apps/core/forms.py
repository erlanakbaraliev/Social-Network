from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

from apps.core.models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        label='',
        max_length=100, 
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
                'autofocus': True
            }
        )
    )
    password = forms.CharField(
        label='',
        max_length=100, 
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password'
            }
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise ValidationError('Incorrect username or password')
            self.user = user
        return cleaned_data


class RegisterForm(forms.Form):
    username = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
                'autofocus': True
            }
        )
    )
    email = forms.EmailField(
        label='',
        max_length=100,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email',
            }
        )
    )
    password = forms.CharField(
        label='',
        max_length=100,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password'
            }
        )
    )
    passwordConfirmation = forms.CharField(
        label='',
        max_length=100,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm Password'
            }
        )
    )

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already exists')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise ValidationError('An account with this email already exists.')
        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data['password']
        passwordConfirmation = cleaned_data['passwordConfirmation']
        
        if password != passwordConfirmation:
            raise ValidationError('Passwords do not match')
        return cleaned_data
    
class PostForm(forms.Form):
    body=forms.CharField(
        label='',
        max_length=1000,
        required=True,
        widget=forms.Textarea(
            attrs={
                'placeholder': "What's happening?"
            }
        )
    )