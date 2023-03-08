"""
This module contains test cases for the accounts application.

The tests cover creation of user with:
    - basic role
    - premium role
    - enterprise role
    - custom role

To run the tests, use the 'python manage.py test accounts/' command.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import Role


class CustomUserTests(TestCase):
    """Test cases for the custom user model."""

    def setUp(self):
        """Set up the test environment."""
        self.User = get_user_model()
        self.basic_role = Role.objects.get(name="Basic")
        self.premium_role = Role.objects.get(name="Premium")
        self.enterprise_role = Role.objects.get(name="Enterprise")
        self.custom_role = Role.objects.create(
            name="custom_role",
            thumbnail_size=213,
            allow_original=False,
            allow_expiring=True,
        )

    def test_create_basic_user(self):
        """Test creation of user with basic role."""
        user = self.User.objects.create_user(
            username="basic_user",
            password="testpass123",
        )
        self.assertEqual(user.username, "basic_user")
        self.assertTrue(user.is_active)
        self.assertEqual(user.role, self.basic_role)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.role.thumbnail_size, 200)
        self.assertFalse(user.role.allow_original)
        self.assertFalse(user.role.allow_expiring)

    def test_create_premium_user(self):
        """Test creation of user with premium role."""
        premium_user = self.User.objects.create_user(
            username="premium_user",
            password="testpass123",
            role=self.premium_role,
        )
        self.assertEqual(premium_user.username, "premium_user")
        self.assertTrue(premium_user.is_active)
        self.assertEqual(premium_user.role, self.premium_role)
        self.assertFalse(premium_user.is_superuser)
        self.assertEqual(premium_user.role.thumbnail_size, 400)
        self.assertTrue(premium_user.role.allow_original)
        self.assertFalse(premium_user.role.allow_expiring)

    def test_create_enterprise_user(self):
        """Test creation of user with enterprise role."""
        enterprise_user = self.User.objects.create_user(
            username="enterprise_user",
            password="testpass123",
            role=self.enterprise_role,
        )
        self.assertEqual(enterprise_user.username, "enterprise_user")
        self.assertTrue(enterprise_user.is_active)
        self.assertEqual(enterprise_user.role, self.enterprise_role)
        self.assertFalse(enterprise_user.is_superuser)
        self.assertEqual(enterprise_user.role.thumbnail_size, 400)
        self.assertTrue(enterprise_user.role.allow_original)
        self.assertTrue(enterprise_user.role.allow_expiring)

    def test_custom_role_user(self):
        """Test creation of user with custom role."""
        custom_role_user = self.User.objects.create_user(
            username="custom_role_user",
            password="testpass123",
            role=self.custom_role,
        )
        self.assertEqual(custom_role_user.username, "custom_role_user")
        self.assertTrue(custom_role_user.is_active)
        self.assertEqual(custom_role_user.role, self.custom_role)
        self.assertFalse(custom_role_user.is_superuser)
        self.assertEqual(custom_role_user.role.thumbnail_size, 213)
        self.assertFalse(custom_role_user.role.allow_original)
        self.assertTrue(custom_role_user.role.allow_expiring)

    def test_create_superuser(self):
        """Test creation of superuser."""
        super_user = self.User.objects.create_superuser(
            username="superuser",
            password="testpass123",
            email="email@email.com",
        )
        self.assertEqual(super_user.username, "superuser")
        self.assertTrue(super_user.is_active)
        self.assertTrue(super_user.is_superuser)
