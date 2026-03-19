from django.utils import timezone
from rest_framework import serializers
from apps.jobs.models import Job, SavedJob


class JobSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    employer_username = serializers.CharField(source='employer.username', read_only=True)

    class Meta:
        model = Job
        fields = [
            'id',
            'title',
            'description',
            'location',
            'job_type',
            'work_mode',
            'employment_type',
            'salary',
            'salary_min',
            'salary_max',
            'status',
            'is_active',
            'created_at',
            'company',
            'company_name',
            'category',
            'category_name',
            'employer',
            'employer_username',
        ]
        read_only_fields = ['employer', 'company', 'created_at']

    def validate(self, attrs):
        salary_min = attrs.get('salary_min')
        salary_max = attrs.get('salary_max')
        deadline = attrs.get('deadline')

        if self.instance:
            salary_min = salary_min if salary_min is not None else self.instance.salary_min
            salary_max = salary_max if salary_max is not None else self.instance.salary_max
            deadline = deadline if deadline is not None else self.instance.deadline

        if (
            salary_min is not None
            and salary_max is not None
            and salary_min > salary_max
        ):
            raise serializers.ValidationError(
                {'salary_max': 'Salary max must be greater than or equal to salary min.'}
            )

        if deadline and deadline < timezone.now().date():
            raise serializers.ValidationError({'deadline': 'Deadline cannot be in the past.'})

        return attrs


class SavedJobSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)

    class Meta:
        model = SavedJob
        fields = ['id', 'job', 'saved_at']
