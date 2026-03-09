from django import forms
from .models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter', 'resume']
        widgets = {
            'cover_letter': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Write a short cover letter'
            }),
            'resume': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }


class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'})
        }