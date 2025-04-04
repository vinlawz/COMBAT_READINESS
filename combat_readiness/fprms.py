# forms.py

from django import forms
from .models import CustomUser

class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role']  # You can include other fields if necessary
