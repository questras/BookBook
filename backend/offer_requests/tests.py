from django.test import TestCase

from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from token_auth.models import AuthToken
from offers.models import Offer
from offers.tests import get_test_offer_data, create_dummy_user, authorize_user

from .models import Request


def get_test_request_data(offer):
    return {
        'offer': offer.id,
        'about': 'test-about',
        'requester_phone': '666555444',
    }


class CreateRequestTests(APITestCase):
    def setUp(self):
        self.url = reverse('request-list')
        self.lender = create_dummy_user(1)
        self.requester = create_dummy_user(2)
        self.offer = Offer.objects.create(lender=self.lender, **get_test_offer_data(1))
        self.data = get_test_request_data(self.offer)

    def test_unauthenticated_cannot_create(self):
        r = self.client.post(self.url, data=self.data)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_correct_data_can_create(self):
        authorize_user(self, self.requester)
        r = self.client.post(self.url, data=self.data)

        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Offer.objects.all().count(), 1)

    def test_cannot_create_twice(self):
        authorize_user(self, self.requester)
        r = self.client.post(self.url, data=self.data)

        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Request.objects.all().count(), 1)

        r = self.client.post(self.url, data=self.data)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Request.objects.all().count(), 1)

    def test_cannot_create_self(self):
        authorize_user(self, self.lender)
        r = self.client.post(self.url, data=self.data)

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Request.objects.all().count(), 0)


class UpdateRequestTest(APITestCase):
    def setUp(self):
        self.lender = create_dummy_user(1)
        self.requester = create_dummy_user(2)
        self.offer = Offer.objects.create(lender=self.lender, **get_test_offer_data(1))
        self.url = reverse('request-detail', args=(self.offer.id, ))
        self.data = get_test_request_data(self.offer)

    def test_unauthenticated_cannot_update(self):
        r = self.client.put(self.url, data=self.data)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_requester_cannot_update(self):
        authorize_user(self, self.lender)

        r = self.client.put(self.url, data=self.data)
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)
