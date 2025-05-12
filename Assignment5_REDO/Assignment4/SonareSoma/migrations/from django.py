from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Professional, User

class ProfessionalViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.professional = Professional.objects.create(user=self.user)

    def test_weekly_summary(self):
        self.client.login(username="testuser", password="password")
        url = reverse('professional-weekly-summary', args=[self.professional.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Weekly summary", response.data["message"])