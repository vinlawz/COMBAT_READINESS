# forms.py

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import CustomUser, UserProfile, Mission, MedicalRecord

class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role']  # You can include other fields if necessary

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image', 'bio']

class MissionForm(forms.ModelForm):
    class Meta:
        model = Mission
        exclude = ['created_by']

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = [
            'blood_type', 'known_allergies', 'current_medications',
            'medical_conditions', 'last_medical_checkup', 'next_checkup_due',
            'status', 'notes'
        ]
        widgets = {
            'last_medical_checkup': forms.DateInput(attrs={'type': 'date'}),
            'next_checkup_due': forms.DateInput(attrs={'type': 'date'}),
            'known_allergies': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'current_medications': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'medical_conditions': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        last_checkup = cleaned_data.get('last_medical_checkup')
        next_checkup = cleaned_data.get('next_checkup_due')
        
        if last_checkup and last_checkup > timezone.now().date():
            raise ValidationError({
                'last_medical_checkup': 'Last medical checkup date cannot be in the future.'
            })
            
        if next_checkup and next_checkup <= timezone.now().date():
            raise ValidationError({
                'next_checkup_due': 'Next checkup must be a future date.'
            })
            
        if last_checkup and next_checkup and next_checkup <= last_checkup:
            raise ValidationError({
                'next_checkup_due': 'Next checkup must be after the last checkup date.'
            })
            
        return cleaned_data
