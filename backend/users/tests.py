from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from token_auth.auth import AuthToken

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


def create_dummy_user(n: int):
    """Create user for testing purposes with
    `n` identifier"""

    return User.objects.create_user(email=f'test{n}@test.com', password='test_password')


def authorize_user(case: APITestCase, user: User):
    token = AuthToken.objects.create(user, 'dummy')
    case.client.credentials(HTTP_AUTHORIZATION=f'Token {token.token}')


class ChangePasswordTests(APITestCase):
    def setUp(self) -> None:
        self.user = create_dummy_user(0)
        self.url = reverse('change-password')
        self.data = {
            'old_password': 'test_password',
            'new_password': 'some_complicated_phrase123'
        }

    def test_not_logged_cannot_access(self):
        r = self.client.put(self.url, self.data)

        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_logged_can_change_password(self):
        authorize_user(self, self.user)

        r = self.client.put(self.url, self.data)

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.data['new_password']))

    def test_cannot_change_with_bad_old_password(self):
        authorize_user(self, self.user)

        self.data['old_password'] = 'bad_old_password'
        r = self.client.put(self.url, self.data)

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(self.user.check_password('test_password'))

    def test_cannot_set_new_password_as_empty(self):
        authorize_user(self, self.user)
        self.data['new_password'] = ''
        r = self.client.put(self.url, self.data)

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(self.user.check_password('test_password'))


register_url = reverse('register')


class APIRegisterTests(APITestCase):
    def setUp(self):
        self.dummy_data = {
            'email': 'dummy@dummy.com',
            'password': 'valid_complicated_password',
            'first_name': 'Dummy',
            'last_name': 'MegaDummy'
        }

    def test_weak_password(self):
        """Reject weak passords"""
        data = self.dummy_data
        data['password'] = 'password'
        response = self.client.post(register_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_creates_user(self):
        """Data integrity test"""
        data = self.dummy_data
        response = self.client.post(register_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

        user = User.objects.get(email=data['email'])
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])
        self.assertTrue(user.check_password(data['password']))

    def test_invalid_data(self):
        """Require valid email and names to be not empty"""
        data = self.dummy_data
        data['email'] = 'invalid'
        data['first_name'] = ''
        data['last_name'] = ''
        response = self.client.post(register_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('last_name', response.data)
        self.assertIn('first_name', response.data)
