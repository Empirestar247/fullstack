from django import forms
from django.contrib.auth.models import User
from .models import Tracking

class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

class TrackingForm(forms.ModelForm):
    class Meta:
        model = Tracking
        fields = ['tracking_number', 'status']
