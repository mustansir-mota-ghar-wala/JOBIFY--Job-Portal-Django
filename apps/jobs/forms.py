from django import forms
from django.utils import timezone
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
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter job title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe the job role, responsibilities and requirements'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter job location'
            }),
            'salary': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter salary'
            }),
            'job_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'deadline': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

        labels = {
            'category': 'Job Category',
            'title': 'Job Title',
            'description': 'Job Description',
            'location': 'Job Location',
            'salary': 'Salary',
            'job_type': 'Job Type',
            'deadline': 'Application Deadline',
            'is_active': 'Active Job Listing'
        }

        help_texts = {
            'deadline': 'Last date candidates can apply.',
            'is_active': 'Uncheck to hide the job listing from public view.'
        }

    def clean_salary(self):
        salary = self.cleaned_data.get('salary')

        if salary in [None, '']:
            return salary

        try:
            salary_value = int(salary)
        except (TypeError, ValueError):
            raise forms.ValidationError('Salary must be a valid number.')

        if salary_value < 0:
            raise forms.ValidationError('Salary cannot be negative.')

        return salary

    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')

        if deadline and deadline < timezone.now().date():
            raise forms.ValidationError('Deadline cannot be in the past.')

        return deadline