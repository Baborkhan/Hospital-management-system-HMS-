"""
MedFind — Account Tests
Tests for user registration, login, JWT token flow.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@medfind.com",
            password="SecurePass@123",
        )

    def test_user_created(self):
        self.assertEqual(User.objects.filter(email="testuser@medfind.com").count(), 1)

    def test_password_hashed(self):
        """Password must NOT be stored in plain text."""
        self.assertNotEqual(self.user.password, "SecurePass@123")
        self.assertTrue(self.user.password.startswith("pbkdf2_") or
                        self.user.password.startswith("argon2") or
                        self.user.password.startswith("bcrypt"))

    def test_is_not_staff_by_default(self):
        self.assertFalse(self.user.is_staff)

    def test_superuser_is_staff(self):
        admin = User.objects.create_superuser(
            email="admin@medfind.com", password="Admin@Secure123"
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
