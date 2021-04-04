from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework import status
from rest_framework.test import APITestCase
from time import sleep

from .models import AuthToken

User = get_user_model()
acquire_url = reverse('acquire_token')
renew_url = reverse('renew_token')
revoke_url = reverse('revoke_token')
register_url = reverse('register')


def _dummy_user():
    return User.objects.create_user(email='dummy@dummy.com', password='dummy')


class AuthTokenTests(TestCase):
    def setUp(self):
        self.device_name = 'Samsung s9'

    def test_create(self):
        user = _dummy_user()
        token = AuthToken.objects.create(user, self.device_name)

        self.assertEqual(token.user.email, user.email)
        self.assertGreater(len(token.token), 40)
        self.assertEqual(token.device, self.device_name)

    def test_invalid_user(self):
        """Test auth to user assigment"""
        with self.assertRaises(IntegrityError):
            AuthToken.objects.create(None, self.device_name)

    def test_no_device(self):
        """Test device requirement"""
        user = _dummy_user()

        with self.assertRaises(IntegrityError):
            AuthToken.objects.create(user, None)

    def test_renew_token(self):
        """Test expirement datetime incremet"""
        user = _dummy_user()
        token = AuthToken.objects.create(user, self.device_name)
        old_expires = token.expires

        sleep(1)
        token.renew()

        self.assertLess(old_expires, token.expires)


class APIAcquireTokenTests(APITestCase):
    def test_returns_token(self):
        """Test valid request and data integrity"""

        user = _dummy_user()
        data = {'email': user.email, 'password': 'dummy', 'device': 'one'}
        response = self.client.post(acquire_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('expires', response.data)
        self.assertIn('token', response.data)

        self.assertEqual(AuthToken.objects.count(), 1)
        auth = AuthToken.objects.get(token=response.data['token'])

        self.assertEqual(response.data['expires'], str(auth.expires))

    def test_bad_password(self):
        """Test password to user matching"""
        user = _dummy_user()
        data = {'email': user.email, 'password': 'invalid', 'device': 'two'}
        response = self.client.post(acquire_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class APIRenewTokenTests(APITestCase):
    def test_unauthorized(self):
        """Test existance of authorization"""
        response = self.client.put(renew_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_token(self):
        """Test handling invalid tokens"""
        self.client.credentials(HTTP_AUTHORIZATION=('Token bad'))
        response = self.client.put(renew_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_extends_lifetime(self):
        """Tests successful auth validation and expire datetime increment"""
        user = _dummy_user()
        token = AuthToken.objects.create(user, 'dummy')
        old_expires = token.expires

        sleep(1)

        self.client.credentials(HTTP_AUTHORIZATION=("Token %s" % token.token))
        response = self.client.put(renew_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('expires', response.data)


class APIRevokeTokenTests(APITestCase):
    def test_invalid(self):
        """Token validation test"""
        data = {'token': 'invalid'}
        response = self.client.post(revoke_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_revokes_token(self):
        """Token removal test"""
        user = _dummy_user()
        auth = AuthToken.objects.create(user, 'dummy')

        self.assertEqual(AuthToken.objects.count(), 1)

        data = {'token': auth.token}
        response = self.client.post(revoke_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(AuthToken.objects.count(), 0)


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
