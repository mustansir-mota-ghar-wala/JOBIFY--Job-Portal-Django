from rest_framework import serializers

from apps.accounts.models import EmployerProfile, SeekerProfile


class EmployerProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)

    class Meta:
        model = EmployerProfile
        fields = [
            'username',
            'email',
            'role',
            'company_name',
            'company_description',
            'website',
            'location',
            'logo',
        ]


class SeekerProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)

    class Meta:
        model = SeekerProfile
        fields = [
            'username',
            'email',
            'role',
            'full_name',
            'skills',
            'education',
            'experience',
            'resume',
            'profile_image',
        ]
