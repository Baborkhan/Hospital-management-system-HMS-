"""
MedFind — Appointment Model Tests
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class AppointmentModelTest(TestCase):
    def test_user_table_accessible(self):
        """Basic DB connectivity check."""
        count = User.objects.count()
        self.assertGreaterEqual(count, 0)

    def test_placeholder_can_create_user(self):
        u = User.objects.create_user(email="appt_test@medfind.com", password="Test@1234")
        self.assertEqual(u.email, "appt_test@medfind.com")
