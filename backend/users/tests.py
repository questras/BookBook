from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserManagerTests(TestCase):
    def test_create_user_correct_fields(self):
        user = User.objects.create_user(email='test@test.com', password='test')

        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_cannot_create_user_without_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='test')

        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, password='test')

    def test_create_superuser_correct_fields(self):
        user = User.objects.create_superuser(
            email='test@test.com', password='test')

        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_cannot_create_superuser_with_false_flags(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='test@test.com', password='test', is_staff=False
            )

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='test@test.com', password='test', is_superuser=False
            )
