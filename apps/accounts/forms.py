from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, EmployerProfile, SeekerProfile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter email'
    }))
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, widget=forms.Select(attrs={
        'class': 'form-select'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter username'
    }))
    password1 = forms.CharField(label='password',widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter password'
    }))
    password2 = forms.CharField(label='confirm password',widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm password'
    }))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter password'
    }))


class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        fields = ['company_name', 'company_description', 'website', 'location', 'logo']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'company_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class SeekerProfileForm(forms.ModelForm):
    class Meta:
        model = SeekerProfile
        fields = ['full_name', 'skills', 'education', 'experience', 'resume', 'profile_image']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'education': forms.TextInput(attrs={'class': 'form-control'}),
            'experience': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'resume': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }