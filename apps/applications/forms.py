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

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')

        if not resume:
            raise forms.ValidationError('Please upload your resume.')

        allowed_extensions = ['pdf', 'doc', 'docx']
        file_extension = resume.name.split('.')[-1].lower()

        if file_extension not in allowed_extensions:
            raise forms.ValidationError('Only PDF, DOC, and DOCX files are allowed.')

        if resume.size > 5 * 1024 * 1024:
            raise forms.ValidationError('Resume file size must be under 5 MB.')

        return resume


class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'})
        }