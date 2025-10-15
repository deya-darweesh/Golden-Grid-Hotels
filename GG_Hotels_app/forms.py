from django import forms
from .models import Room, Service, Booking, Booking_Service
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from datetime import date

class CustomUserSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class UserSignInForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class CustomHotelSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label="Hotel Name")
    last_name = forms.CharField(max_length=30, initial="Hotel", widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['last_name'].help_text = "This field is automatically set to 'Hotel'"
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = "Hotel"
        user.is_staff = True
        if commit:
            user.save()
        return user


class HotelSignInForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_type', 'price_per_night', 'capacity', 'description', 'quantity']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'room_type': forms.Select(choices=[
                ('Single', 'Single'),
                ('Double', 'Double'),
                ('Triple', 'Triple'),
                ('VIP', 'VIP')
            ])
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['room_type'].help_text = None
        self.fields['price_per_night'].help_text = "Price per night in USD"
        self.fields['capacity'].help_text = "Number of people"

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'price', 'description', 'available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['price'].help_text = "Price in USD"


class BookingForm(forms.ModelForm):
    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.filter(available=True),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text="Select additional services (optional)"
    )
    
    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_out_date']
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date', 'min': date.today()}),
            'check_out_date': forms.DateInput(attrs={'type': 'date', 'min': date.today()}),
        }
    
    def __init__(self, *args, **kwargs):
        self.room = kwargs.pop('room', None)
        super().__init__(*args, **kwargs)
        self.fields['check_in_date'].help_text = "Select your check-in date"
        self.fields['check_out_date'].help_text = "Select your check-out date"
        
        if self.data.get('check_in_date'):
            try:
                check_in = date.fromisoformat(self.data['check_in_date'])
                self.fields['check_out_date'].widget.attrs['min'] = check_in
            except ValueError:
                pass
    
    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in_date')
        check_out = cleaned_data.get('check_out_date')
        
        if check_in and check_out:
            if check_out <= check_in:
                raise forms.ValidationError("Check-out date must be after check-in date.")
            
            if check_in < date.today():
                raise forms.ValidationError("Check-in date cannot be in the past.")
        
        return cleaned_data
