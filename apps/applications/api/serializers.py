from rest_framework import serializers
from apps.applications.models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)
    applicant_username = serializers.CharField(source='applicant.username', read_only=True)
    company_name = serializers.CharField(source='job.company.name', read_only=True)

    class Meta:
        model = Application
        fields = [
            'id',
            'job',
            'job_title',
            'applicant',
            'applicant_username',
            'company_name',
            'cover_letter',
            'resume',
            'status',
            'applied_at',
            'updated_at',
        ]
        read_only_fields = ['job', 'applicant', 'status', 'applied_at', 'updated_at']

    def validate_resume(self, resume):
        if not resume:
            raise serializers.ValidationError('Please upload your resume.')

        allowed_extensions = {'pdf', 'doc', 'docx'}
        file_extension = resume.name.split('.')[-1].lower()

        if file_extension not in allowed_extensions:
            raise serializers.ValidationError('Only PDF, DOC, and DOCX files are allowed.')

        if resume.size > 5 * 1024 * 1024:
            raise serializers.ValidationError('Resume file size must be under 5 MB.')

        return resume

class ApplicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['status']
