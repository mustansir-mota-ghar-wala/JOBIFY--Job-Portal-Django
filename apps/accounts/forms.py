from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, EmployerProfile, SeekerProfile


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username'
        })
    )

    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email'
        })
    )

    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )

    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise forms.ValidationError('Username must be at least 3 characters long.')
        return username


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username'
        })
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )


class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        fields = ['company_name', 'company_description', 'website', 'location', 'logo']
        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company name'
            }),
            'company_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write a short company description'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company website'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company location'
            }),
            'logo': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

    def clean_logo(self):
        logo = self.cleaned_data.get('logo')
        if logo:
            allowed_extensions = ['jpg', 'jpeg', 'png', 'webp']
            file_extension = logo.name.split('.')[-1].lower()

            if file_extension not in allowed_extensions:
                raise forms.ValidationError('Only JPG, JPEG, PNG, and WEBP image files are allowed.')

            if logo.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Logo file size must be under 3 MB.')
        return logo


class SeekerProfileForm(forms.ModelForm):
    class Meta:
        model = SeekerProfile
        fields = ['full_name', 'skills', 'education', 'experience', 'resume', 'profile_image']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full name'
            }),
            'skills': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter your skills'
            }),
            'education': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your education'
            }),
            'experience': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter your experience'
            }),
            'resume': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'profile_image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            allowed_extensions = ['pdf', 'doc', 'docx']
            file_extension = resume.name.split('.')[-1].lower()

            if file_extension not in allowed_extensions:
                raise forms.ValidationError('Only PDF, DOC, and DOCX files are allowed.')

            if resume.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Resume file size must be under 5 MB.')
        return resume

    def clean_profile_image(self):
        profile_image = self.cleaned_data.get('profile_image')
        if profile_image:
            allowed_extensions = ['jpg', 'jpeg', 'png', 'webp']
            file_extension = profile_image.name.split('.')[-1].lower()

            if file_extension not in allowed_extensions:
                raise forms.ValidationError('Only JPG, JPEG, PNG, and WEBP image files are allowed.')

            if profile_image.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Profile image size must be under 3 MB.')
        return profile_image