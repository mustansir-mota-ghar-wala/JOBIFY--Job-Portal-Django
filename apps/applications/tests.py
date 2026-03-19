from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from apps.accounts.models import Company, CustomUser
from apps.applications.models import Application
from apps.jobs.models import Job


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class ApplicationFlowTests(TestCase):
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
        self.other_employer = CustomUser.objects.create_user(
            username='employer2',
            email='other@example.com',
            password='StrongPass123',
            role='employer',
        )
        self.company = Company.objects.create(
            name='Acme Inc',
            created_by=self.employer,
        )
        self.job = Job.objects.create(
            employer=self.employer,
            company=self.company,
            title='Python Developer',
            description='Build Django apps',
            location='Remote',
            is_active=True,
        )

    def _resume_file(self, name='resume.pdf'):
        return SimpleUploadedFile(name, b'%PDF-1.4 test resume content', content_type='application/pdf')

    def test_seeker_can_apply_once(self):
        self.client.login(username='seeker1', password='StrongPass123')

        response = self.client.post(
            reverse('apply_job', args=[self.job.id]),
            {
                'cover_letter': 'I would love to contribute.',
                'resume': self._resume_file(),
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Application.objects.filter(job=self.job, applicant=self.seeker).count(), 1)

        duplicate_response = self.client.post(
            reverse('apply_job', args=[self.job.id]),
            {
                'cover_letter': 'Trying to apply again.',
                'resume': self._resume_file('resume2.pdf'),
            },
        )

        self.assertEqual(duplicate_response.status_code, 302)
        self.assertEqual(Application.objects.filter(job=self.job, applicant=self.seeker).count(), 1)

    def test_employer_can_update_only_own_application(self):
        application = Application.objects.create(
            job=self.job,
            applicant=self.seeker,
            cover_letter='Hello',
            resume=self._resume_file(),
        )

        self.client.login(username='employer1', password='StrongPass123')
        response = self.client.post(
            reverse('update_application_status', args=[application.id]),
            {'status': 'reviewed'},
        )

        self.assertEqual(response.status_code, 302)
        application.refresh_from_db()
        self.assertEqual(application.status, 'reviewed')

        self.client.login(username='employer2', password='StrongPass123')
        forbidden_response = self.client.get(reverse('update_application_status', args=[application.id]))
        self.assertEqual(forbidden_response.status_code, 404)


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class ApplicationApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.employer = CustomUser.objects.create_user(
            username='api_employer1',
            email='api_employer1@example.com',
            password='StrongPass123',
            role='employer',
        )
        self.seeker = CustomUser.objects.create_user(
            username='api_seeker1',
            email='api_seeker1@example.com',
            password='StrongPass123',
            role='seeker',
        )
        self.company = Company.objects.create(name='Acme API', created_by=self.employer)
        self.job = Job.objects.create(
            employer=self.employer,
            company=self.company,
            title='API Python Developer',
            description='Build Django APIs',
            location='Remote',
            status='published',
            is_active=True,
        )
        self.draft_job = Job.objects.create(
            employer=self.employer,
            company=self.company,
            title='Draft API Job',
            description='Not open yet',
            location='Remote',
            status='draft',
            is_active=True,
        )

    def _resume_file(self, name='resume.pdf'):
        return SimpleUploadedFile(name, b'%PDF-1.4 api resume content', content_type='application/pdf')

    def test_seeker_can_apply_once_via_api(self):
        self.client.login(username='api_seeker1', password='StrongPass123')

        response = self.client.post(
            reverse('api_apply_job', args=[self.job.id]),
            {'cover_letter': 'Interested', 'resume': self._resume_file()},
        )
        self.assertEqual(response.status_code, 201)

        duplicate_response = self.client.post(
            reverse('api_apply_job', args=[self.job.id]),
            {'cover_letter': 'Interested again', 'resume': self._resume_file('resume2.pdf')},
        )
        self.assertEqual(duplicate_response.status_code, 400)
        self.assertEqual(Application.objects.filter(job=self.job, applicant=self.seeker).count(), 1)

    def test_seeker_cannot_apply_to_draft_job_via_api(self):
        self.client.login(username='api_seeker1', password='StrongPass123')

        response = self.client.post(
            reverse('api_apply_job', args=[self.draft_job.id]),
            {'cover_letter': 'Interested', 'resume': self._resume_file()},
        )

        self.assertEqual(response.status_code, 404)

    def test_employer_can_update_application_status_via_api(self):
        application = Application.objects.create(
            job=self.job,
            applicant=self.seeker,
            cover_letter='Hello',
            resume=self._resume_file(),
        )
        self.client.login(username='api_employer1', password='StrongPass123')

        response = self.client.patch(
            reverse('api_update_application_status', args=[application.id]),
            {'status': 'shortlisted'},
            format='json',
        )

        self.assertEqual(response.status_code, 200)
        application.refresh_from_db()
        self.assertEqual(application.status, 'shortlisted')
