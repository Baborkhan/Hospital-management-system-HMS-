"""
MedFind — Hospital Tests
"""
from django.test import TestCase


class HospitalAppTest(TestCase):
    def test_app_loads(self):
        """Check the hospitals app is installed and importable."""
        try:
            from apps.hospitals.models import Hospital
            self.assertTrue(True)
        except ImportError:
            self.fail("hospitals app not importable — check INSTALLED_APPS")
