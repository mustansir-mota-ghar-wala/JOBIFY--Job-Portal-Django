from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.accounts.models import Company, CustomUser
from apps.jobs.models import Job, SavedJob


class SavedJobFlowTests(TestCase):
    def setUp(self):
        self.employer = CustomUser.objects.create_user(
            username='employer1',
            email='employer@example.com',
            password='StrongPass123',
            role='employer',
        )
        self.seeker = CustomUser.objects.create_user(
            username='seeker1',
            email='seeker@example.com',
            password='StrongPass123',
            role='seeker',
        )
        self.company = Company.objects.create(
            name='Acme Inc',
            created_by=self.employer,
        )
        self.job = Job.objects.create(
            employer=self.employer,
            company=self.company,
            title='Backend Developer',
            description='Build backend services',
            location='Bengaluru',
            status='published',
            is_active=True,
        )

    def test_seeker_can_save_and_unsave_job(self):
        self.client.login(username='seeker1', password='StrongPass123')

        save_response = self.client.get(reverse('save_job', args=[self.job.id]))
        self.assertEqual(save_response.status_code, 302)
        self.assertTrue(SavedJob.objects.filter(user=self.seeker, job=self.job).exists())

        unsave_response = self.client.get(reverse('unsave_job', args=[self.job.id]))
        self.assertEqual(unsave_response.status_code, 302)
        self.assertFalse(SavedJob.objects.filter(user=self.seeker, job=self.job).exists())

    def test_job_list_shows_active_job(self):
        response = self.client.get(reverse('job_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Backend Developer')


class JobApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.employer = CustomUser.objects.create_user(
            username='api_employer',
            email='api_employer@example.com',
            password='StrongPass123',
            role='employer',
        )
        self.other_employer = CustomUser.objects.create_user(
            username='other_employer',
            email='other_employer@example.com',
            password='StrongPass123',
            role='employer',
        )
        self.seeker = CustomUser.objects.create_user(
            username='api_seeker',
            email='api_seeker@example.com',
            password='StrongPass123',
            role='seeker',
        )
        self.company = Company.objects.create(name='API Co', created_by=self.employer)
        self.published_job = Job.objects.create(
            employer=self.employer,
            company=self.company,
            title='Published Job',
            description='Visible to the public',
            location='Remote',
            status='published',
            is_active=True,
        )
        self.draft_job = Job.objects.create(
            employer=self.employer,
            company=self.company,
            title='Draft Job',
            description='Should stay hidden',
            location='Remote',
            status='draft',
            is_active=True,
        )

    def test_public_jobs_api_hides_draft_jobs(self):
        response = self.client.get(reverse('api_job_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Published Job')
        self.assertNotContains(response, 'Draft Job')

    def test_employer_can_create_job_via_api(self):
        self.client.login(username='api_employer', password='StrongPass123')

        response = self.client.post(
            reverse('api_job_create'),
            {
                'title': 'API Created Job',
                'description': 'Created through DRF',
                'location': 'Pune',
                'status': 'published',
                'is_active': True,
            },
            format='json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Job.objects.filter(title='API Created Job', employer=self.employer).exists())

    def test_seeker_cannot_create_job_via_api(self):
        self.client.login(username='api_seeker', password='StrongPass123')

        response = self.client.post(
            reverse('api_job_create'),
            {
                'title': 'Blocked Job',
                'description': 'Should not be created',
                'location': 'Pune',
            },
            format='json',
        )

        self.assertEqual(response.status_code, 403)

    def test_job_owner_only_can_manage_job(self):
        self.client.login(username='other_employer', password='StrongPass123')

        response = self.client.patch(
            reverse('api_job_manage', args=[self.published_job.id]),
            {'title': 'Updated by intruder'},
            format='json',
        )

        self.assertEqual(response.status_code, 403)

    def test_employer_can_list_own_jobs_via_api(self):
        self.client.login(username='api_employer', password='StrongPass123')

        response = self.client.get(reverse('api_employer_job_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Published Job')
        self.assertContains(response, 'Draft Job')

    def test_seeker_can_list_saved_jobs_via_api(self):
        SavedJob.objects.create(user=self.seeker, job=self.published_job)
        self.client.login(username='api_seeker', password='StrongPass123')

        response = self.client.get(reverse('api_saved_job_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Published Job')
