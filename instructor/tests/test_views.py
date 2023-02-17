from django.test import TestCase
from django.urls import reverse


class InstructorTestCase(TestCase):
    def test_dashboard(self):
        response = self.client.get(reverse("instructor-dashboard"))
        self.assertEqual(response.status_code, 302)
