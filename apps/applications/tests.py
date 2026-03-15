from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

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

    def test_resume_link_normalizes_legacy_media_prefix(self):
        application = Application.objects.create(
            job=self.job,
            applicant=self.seeker,
            cover_letter='Hello',
            resume=self._resume_file(),
        )
        application.resume.name = 'media/application_resumes/resume.pdf'

        self.assertEqual(application.resume_link, '/media/application_resumes/resume.pdf')
