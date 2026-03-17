"""
accounts/forms.py
------------------
Forms for registration and profile editing.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import UserProfile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model  = User
        fields = ['username', 'email', 'password1', 'password2']


class UserInfoForm(forms.ModelForm):
    """Lets the user edit their first name, last name, and email."""
    class Meta:
        model  = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
            'last_name':  forms.TextInput(attrs={'placeholder': 'Last name'}),
            'email':      forms.EmailInput(attrs={'placeholder': 'your@email.com'}),
        }


class ProfileForm(forms.ModelForm):
    """Lets the user update their fitness goal."""
    class Meta:
        model  = UserProfile
        fields = ['fitness_goal']
        widgets = {
            'fitness_goal': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'e.g. Run a 5K by June, lose 10kg by December...'
            }),
        }
