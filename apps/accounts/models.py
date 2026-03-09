from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('employer','Employer'),
        ('seeker','Seeker'),
    )
    role = models.CharField(max_length=200,choices=ROLE_CHOICES)

    def __str__(self):
        return self.username

class EmployerProfile(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='employer_profile')
    company_name = models.CharField(max_length=200)
    company_description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    logo = models.ImageField(upload_to='profile_pics/',blank=True,null=True)

    def __str__(self):
        return self.company_name
    
class SeekerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='seeker_profile')
    full_name = models.CharField(max_length=200)
    skills = models.TextField(blank=True, null=True)
    education = models.CharField(max_length=200, blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.full_name