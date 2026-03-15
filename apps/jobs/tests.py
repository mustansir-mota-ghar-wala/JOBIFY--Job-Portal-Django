from django.test import TestCase
from django.urls import reverse

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
