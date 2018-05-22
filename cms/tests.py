
from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
# Create your tests here.

class PdfTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):

        User.objects.create_superuser('me', 'me@example.org', 'mepassword')

    def setUp(self):
        self.client.login(username='me', password='mepassword')

    def test_plan_pdf(self):
        response = self.client.get(reverse('plan-pdf'))
        self.assertEqual(
            response['Content-Disposition'],
            'attachment; filename="plan_formation.pdf"'
        )
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertGreater(len(response.content), 200)
