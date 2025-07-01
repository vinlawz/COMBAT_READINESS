# forms.py

from django import forms
from .models import CustomUser, UserProfile

class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role']  # You can include other fields if necessary

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image', 'bio']
