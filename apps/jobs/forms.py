from django import forms
from .models import Job


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'category',
            'title',
            'description',
            'location',
            'salary',
            'job_type',
            'deadline',
            'is_active',
        ]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter job title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Enter job description'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter location'}),
            'salary': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter salary'}),
            'job_type': forms.Select(attrs={'class': 'form-select'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }