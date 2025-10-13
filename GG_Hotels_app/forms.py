from django import forms
from .models import Room, Service, Booking, Booking_Service
from django.contrib.auth.models import User

# my forms

class UserSignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput,
        }
        error_messages = {
            'username': {
                'unique': 'This username is already taken. Please choose another one.',
            }
        }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            self.add_error('email', 'This email is already registered. Please use a different email.')
        return cleaned_data

class UserSignInForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'password': forms.PasswordInput,
        }
        error_messages = {
            'email': {
                'required': 'Please enter your email address.',
                'invalid': 'Please enter a valid email address.'
            },
            'password': {
                'required': 'Please enter your password.'
            }
        }
