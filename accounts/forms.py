"""
Authentication forms: Registration, Login, and Profile management.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class RegistrationForm(UserCreationForm):
    """User registration form with role selection."""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your email',
            'id': 'reg-email'
        })
    )
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'First name',
            'id': 'reg-first-name'
        })
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Last name',
            'id': 'reg-last-name'
        })
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Phone number (optional)',
            'id': 'reg-phone'
        })
    )
    location = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Your location (optional)',
            'id': 'reg-location'
        })
    )
    role = forms.ChoiceField(
        choices=[('farmer', 'Farmer'), ('admin', 'Admin')],
        widget=forms.Select(attrs={
            'class': 'form-input',
            'id': 'reg-role'
        })
    )

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'phone', 'location', 'role', 'password1', 'password2'
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Choose a username',
                'id': 'reg-username'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Create a password',
            'id': 'reg-password1'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Confirm password',
            'id': 'reg-password2'
        })


class LoginForm(AuthenticationForm):
    """Custom login form with styled inputs."""

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Username',
            'id': 'login-username',
            'autofocus': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Password',
            'id': 'login-password'
        })
    )


class ProfileForm(forms.ModelForm):
    """Profile update form."""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'location', 'profile_image']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'id': 'profile-first-name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'id': 'profile-last-name'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'id': 'profile-email'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'id': 'profile-phone'}),
            'location': forms.TextInput(attrs={'class': 'form-input', 'id': 'profile-location'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-input', 'id': 'profile-image'}),
        }
