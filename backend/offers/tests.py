from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from .models import Offer
from token_auth.models import AuthToken

User = get_user_model()

incorrect_phone_numbers = (
    '1231231231',  # too long
    '12312312',  # too short
    '123123a12',  # incorrect character
    '+38 123123123',  # incorrect country code
    '+123123123',  # + but without country code
)


def create_dummy_user(n: int):
    """Create user for testing purposes with
    `n` identifier"""

    return User.objects.create_user(email=f'test{n}@test.com', password='test_password')


def authorize_user(case: APITestCase, user: User):
    token = AuthToken.objects.create(user, 'dummy')
    case.client.credentials(HTTP_AUTHORIZATION=f'Token {token.token}')


class CreateOfferTests(APITestCase):
    def setUp(self) -> None:
        self.url = reverse('offer-list')
        self.user = create_dummy_user(1)
        self.data = {
            'author': 'test-author',
            'city': 'test-city',
            'description': 'test-description',
            'lender_phone': '666555444',
            'state': 'test-state',
            'title': 'test-title'
        }

    def test_unauthenticated_cannot_create(self):
        r = self.client.post(self.url, data=self.data)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_correct_data_can_create(self):
        authorize_user(self, self.user)
        r = self.client.post(self.url, data=self.data)

        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Offer.objects.all().count(), 1)

    def test_cannot_create_bad_phone(self):
        authorize_user(self, self.user)

        for incorrect_phone in incorrect_phone_numbers:
            self.data['lender_phone'] = incorrect_phone

            r = self.client.post(self.url, data=self.data)
            self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(Offer.objects.all().count(), 0)

    def test_cannot_create_with_incomplete_data(self):
        authorize_user(self, self.user)

        for field in self.data.keys():
            data_copy = self.data.copy()
            data_copy.pop(field)  # remove field from data

            r = self.client.post(self.url, data=data_copy)
            self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(Offer.objects.all().count(), 0)

    def test_cannot_explicitly_set_status_during_creation(self):
        authorize_user(self, self.user)
        self.data['status'] = 'LT'  # set status in data as 'Lent'

        r = self.client.post(self.url, data=self.data)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        offers = Offer.objects.all()
        self.assertEqual(offers.count(), 1)
        # status is set as 'Active' anyway
        self.assertEqual(offers[0].status, 'AC')


class UpdateOfferTests(APITestCase):
    def setUp(self) -> None:
        self.user = create_dummy_user(1)
        self.data = {
            'author': 'test-author',
            'city': 'test-city',
            'description': 'test-description',
            'lender_phone': '666555444',
            'state': 'test-state',
            'title': 'test-title'
        }
        self.offer = Offer.objects.create(lender=self.user, **self.data)
        self.url = reverse('offer-detail', args=(self.offer.id,))

    def test_unauthenticated_cannot_update(self):
        r = self.client.put(self.url, data=self.data)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_lender_cannot_update(self):
        not_lender = create_dummy_user(2)
        authorize_user(self, not_lender)

        r = self.client.put(self.url, data=self.data)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_correct_data_can_update(self):
        authorize_user(self, self.user)

        # Change data to update
        for key, value in self.data.items():
            if key == 'lender_phone':
                self.data[key] = '111111111'
                continue

            self.data[key] = value + 'updated'

        r = self.client.put(self.url, data=self.data)
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        # Get updated offer.
        offer = Offer.objects.get(pk=self.offer.id)
        for key, value in self.data.items():
            self.assertEqual(getattr(offer, key), value)

    def test_cannot_update_bad_phone(self):
        authorize_user(self, self.user)

        old_phone = self.data['lender_phone']
        for incorrect_phone in incorrect_phone_numbers:
            self.data['lender_phone'] = incorrect_phone

            r = self.client.put(self.url, data=self.data)
            self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
            updated_offer = Offer.objects.get(pk=self.offer.id)
            self.assertEqual(updated_offer.lender_phone, old_phone)

    def test_cannot_partially_update_with_put(self):
        authorize_user(self, self.user)

        for field in self.data.keys():
            data_copy = self.data.copy()
            data_copy.pop(field)  # remove field from data

            r = self.client.put(self.url, data=data_copy)
            self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_explicitly_set_status_during_update(self):
        authorize_user(self, self.user)
        self.data['status'] = 'LT'  # set status in data as 'Lent'

        r = self.client.put(self.url, data=self.data)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        offers = Offer.objects.all()
        # status is set as 'Active' anyway
        self.assertEqual(offers[0].status, 'AC')


class PartialUpdateOfferTests(APITestCase):
    def setUp(self) -> None:
        self.user = create_dummy_user(1)
        self.data = {
            'author': 'test-author',
            'city': 'test-city',
            'description': 'test-description',
            'lender_phone': '666555444',
            'state': 'test-state',
            'title': 'test-title'
        }
        self.offer = Offer.objects.create(lender=self.user, **self.data)
        self.url = reverse('offer-detail', args=(self.offer.id,))

    def test_unauthenticated_cannot_update(self):
        r = self.client.patch(self.url, data=self.data)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_lender_cannot_update(self):
        not_lender = create_dummy_user(2)
        authorize_user(self, not_lender)

        r = self.client.patch(self.url, data=self.data)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_correct_data_can_update(self):
        authorize_user(self, self.user)

        # Partially update each field
        for key, value in self.data.items():
            update_data = dict()
            if key == 'lender_phone':
                update_data[key] = '111111111'
            else:
                update_data[key] = value + 'updated'

            r = self.client.patch(self.url, data=update_data)
            self.assertEqual(r.status_code, status.HTTP_200_OK)

            # Get updated offer.
            offer = Offer.objects.get(pk=self.offer.id)
            self.assertEqual(getattr(offer, key), update_data[key])

    def test_cannot_update_bad_phone(self):
        authorize_user(self, self.user)

        old_phone = self.data['lender_phone']
        update_data = dict()
        for incorrect_phone in incorrect_phone_numbers:
            update_data['lender_phone'] = incorrect_phone

            r = self.client.patch(self.url, data=update_data)
            self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
            updated_offer = Offer.objects.get(pk=self.offer.id)
            self.assertEqual(updated_offer.lender_phone, old_phone)

    def test_cannot_explicitly_set_status_during_update(self):
        authorize_user(self, self.user)
        update_data = {'status': 'LT'}  # set status in data as 'Lent'

        r = self.client.patch(self.url, data=update_data)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        offers = Offer.objects.all()
        # status is set as 'Active' anyway
        self.assertEqual(offers[0].status, 'AC')


class DeleteOfferTests(APITestCase):
    def setUp(self) -> None:
        self.user = create_dummy_user(1)
        self.data = {
            'author': 'test-author',
            'city': 'test-city',
            'description': 'test-description',
            'lender_phone': '666555444',
            'state': 'test-state',
            'title': 'test-title'
        }
        self.offer = Offer.objects.create(lender=self.user, **self.data)
        self.url = reverse('offer-detail', args=(self.offer.id,))

    def test_unauthenticated_cannot_delete(self):
        r = self.client.delete(self.url)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_lender_cannot_delete(self):
        not_lender = create_dummy_user(2)
        authorize_user(self, not_lender)

        r = self.client.delete(self.url)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_lender_can_delete(self):
        authorize_user(self, self.user)

        r = self.client.delete(self.url)
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Offer.objects.all().count(), 0)


class ReadOfferTests(APITestCase):
    def setUp(self) -> None:
        self.user = create_dummy_user(1)
        self.data = {
            'author': 'test-author',
            'city': 'test-city',
            'description': 'test-description',
            'lender_phone': '666555444',
            'state': 'test-state',
            'title': 'test-title'
        }
        self.data2 = {
            'author': 'test-author2',
            'city': 'test-city2',
            'description': 'test-description2',
            'lender_phone': '098890765',
            'state': 'test-state2',
            'title': 'test-title2'
        }
        self.offer = Offer.objects.create(lender=self.user, **self.data)
        self.offer2 = Offer.objects.create(lender=self.user, **self.data2)
        self.url = reverse('offer-detail', args=(self.offer.id,))
        self.list_url = reverse('offer-list')

    def test_unauthenticated_cannot_read(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        r = self.client.get(self.list_url)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_can_read(self):
        authorize_user(self, self.user)

        # single object
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        offer = r.json()
        for field, value in self.data.items():
            self.assertEqual(offer[field], value)

        # list of objects
        r = self.client.get(self.list_url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        offers = r.json()
        self.assertEqual(len(offers), 2)

        offer = offers[0]
        for field, value in self.data.items():
            self.assertEqual(offer[field], value)

        offer2 = offers[1]
        for field, value in self.data2.items():
            self.assertEqual(offer2[field], value)
