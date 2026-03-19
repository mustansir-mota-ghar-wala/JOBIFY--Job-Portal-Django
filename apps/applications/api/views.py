from django.shortcuts import get_object_or_404
from rest_framework import generics, parsers
from rest_framework.exceptions import ValidationError

from apps.applications.models import Application
from apps.jobs.api.permissions import IsEmployer, IsSeeker
from apps.jobs.models import Job

from .serializers import ApplicationSerializer, ApplicationStatusSerializer


class ApplyJobAPIView(generics.CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsSeeker]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def perform_create(self, serializer):
        job = get_object_or_404(
            Job,
            id=self.kwargs['id'],
            is_active=True,
            status='published',
        )

        if Application.objects.filter(job=job, applicant=self.request.user).exists():
            raise ValidationError({'detail': 'You have already applied for this job.'})

        serializer.save(job=job, applicant=self.request.user)


class MyApplicationsAPIView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsSeeker]

    def get_queryset(self):
        return (
            Application.objects
            .filter(applicant=self.request.user)
            .select_related('job', 'job__company', 'job__category', 'applicant')
            .order_by('-applied_at')
        )


class EmployerApplicationsAPIView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsEmployer]

    def get_queryset(self):
        return (
            Application.objects
            .filter(job__employer=self.request.user)
            .select_related('job', 'job__company', 'job__category', 'applicant')
            .order_by('-applied_at')
        )


class UpdateApplicationStatusAPIView(generics.UpdateAPIView):
    serializer_class = ApplicationStatusSerializer
    permission_classes = [IsEmployer]
    lookup_field = 'id'

    def get_queryset(self):
        return (
            Application.objects
            .filter(job__employer=self.request.user)
            .select_related('job', 'job__company', 'applicant')
        )
