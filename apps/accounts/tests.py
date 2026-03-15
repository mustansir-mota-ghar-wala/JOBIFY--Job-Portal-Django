from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import CustomUser, SeekerProfile


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
