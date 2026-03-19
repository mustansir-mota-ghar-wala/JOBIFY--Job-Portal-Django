from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.accounts.models import Company, CustomUser, EmployerProfile, SeekerProfile


class SeekerDashboardTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='seeker1',
            email='seeker@example.com',
            password='StrongPass123',
            role='seeker',
        )
        SeekerProfile.objects.create(
            user=self.user,
            full_name='Seeker One',
            skills='Python, Django',
            education='MCA',
        )

    def test_seeker_dashboard_requires_login(self):
        response = self.client.get(reverse('seeker_dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_seeker_dashboard_renders_completion_data(self):
        self.client.login(username='seeker1', password='StrongPass123')

        response = self.client.get(reverse('seeker_dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['profile_completion'], 60)
        self.assertEqual(response.context['completed_items'], 3)
        self.assertContains(response, 'Seeker workspace')


class ProfileApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.seeker = CustomUser.objects.create_user(
            username='seeker_api',
            email='seeker_api@example.com',
            password='StrongPass123',
            role='seeker',
        )
        SeekerProfile.objects.create(user=self.seeker, full_name='Seeker Api')
        self.employer = CustomUser.objects.create_user(
            username='employer_api',
            email='employer_api@example.com',
            password='StrongPass123',
            role='employer',
        )
        EmployerProfile.objects.create(user=self.employer, company_name='Employer API Co')
        Company.objects.create(name='Employer API Co', created_by=self.employer)

    def test_seeker_profile_api_returns_seeker_profile(self):
        self.client.login(username='seeker_api', password='StrongPass123')

        response = self.client.get(reverse('api_my_profile'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['role'], 'seeker')
        self.assertEqual(response.data['full_name'], 'Seeker Api')

    def test_employer_profile_patch_keeps_company_in_sync(self):
        self.client.login(username='employer_api', password='StrongPass123')

        response = self.client.patch(
            reverse('api_my_profile'),
            {'company_name': 'Updated Employer API Co', 'location': 'Mumbai'},
            format='json',
        )

        self.assertEqual(response.status_code, 200)
        company = self.employer.companies.first()
        self.assertEqual(company.name, 'Updated Employer API Co')
        self.assertEqual(company.location, 'Mumbai')
