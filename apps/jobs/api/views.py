from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from apps.accounts.models import Company
from apps.jobs.models import Job, SavedJob
from .permissions import IsEmployer, IsJobOwner, IsSeeker
from .serializers import JobSerializer, SavedJobSerializer



class JobListAPIView(generics.ListAPIView):
    serializer_class = JobSerializer

    def get_queryset(self):
        jobs = (
            Job.objects
            .filter(is_active=True, status='published')
            .select_related('company', 'category', 'employer')
            .order_by('-created_at')
        )

        keyword = self.request.GET.get('keyword', '')
        category_id = self.request.GET.get('category', '')
        location = self.request.GET.get('location', '')
        job_type = self.request.GET.get('job_type', '')

        if keyword:
            jobs = jobs.filter(
                Q(title__icontains=keyword) |
                Q(description__icontains=keyword) |
                Q(location__icontains=keyword)
            )

        if category_id:
            jobs = jobs.filter(category_id=category_id)

        if location:
            jobs = jobs.filter(location__icontains=location)

        if job_type:
            jobs = jobs.filter(job_type=job_type)

        return jobs


class JobDetailAPIView(generics.RetrieveAPIView):
    serializer_class = JobSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return (
            Job.objects
            .filter(is_active=True, status='published')
            .select_related('company', 'category', 'employer')
        )


class JobCreateAPIView(generics.CreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsEmployer]

    def perform_create(self, serializer):
        company = self.request.user.companies.first()

        if not company:
            company = Company.objects.create(
                name=self.request.user.username,
                created_by=self.request.user
            )

        serializer.save(
            employer=self.request.user,
            company=company
        )


class EmployerJobListAPIView(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsEmployer]

    def get_queryset(self):
        return (
            Job.objects
            .filter(employer=self.request.user)
            .select_related('company', 'category', 'employer')
            .order_by('-created_at')
        )


class JobUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsEmployer, IsJobOwner]
    lookup_field = 'id'

    def get_queryset(self):
        return (
            Job.objects
            .select_related('company', 'category', 'employer')
        )

class SaveJobAPIView(generics.GenericAPIView):
    permission_classes = [IsSeeker]

    def post(self, request, id):
        job = get_object_or_404(Job, id=id, is_active=True, status='published')
        saved_job, created = SavedJob.objects.get_or_create(user=request.user, job=job)

        if created:
            return Response(
                {'message': 'Job saved successfully.'},
                status=status.HTTP_201_CREATED
            )

        return Response(
            {'message': 'Job is already saved.'},
            status=status.HTTP_200_OK
        )


class SavedJobListAPIView(generics.ListAPIView):
    serializer_class = SavedJobSerializer
    permission_classes = [IsSeeker]

    def get_queryset(self):
        return (
            SavedJob.objects
            .filter(user=self.request.user)
            .select_related('job', 'job__company', 'job__category', 'job__employer')
            .order_by('-saved_at')
        )


class UnsaveJobAPIView(generics.GenericAPIView):
    permission_classes = [IsSeeker]

    def delete(self, request, id):
        job = get_object_or_404(Job, id=id, is_active=True, status='published')
        saved_job = SavedJob.objects.filter(user=request.user, job=job).first()

        if saved_job:
            saved_job.delete()
            return Response(
                {'message': 'Saved job removed successfully.'},
                status=status.HTTP_200_OK
            )

        return Response(
            {'message': 'This job was not in your saved list.'},
            status=status.HTTP_200_OK
        )
