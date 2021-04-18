from tempfile import NamedTemporaryFile

from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from PIL import Image

from .models import Offer, OfferImage
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


def get_test_offer_data(n: int):
    """Return data needed to create instance of offer model
    for testing purposes with `n` identifier"""

    return {
        'author': f'test-author{n}',
        'city': f'test-city{n}',
        'description': f'test-description{n}',
        'lender_phone': '666555444',
        'state': f'test-state{n}',
        'title': f'test-title{n}'
    }


def get_temp_image_file():
    """Get temporary image file object for testing purposes"""

    temp_image = NamedTemporaryFile(suffix='.jpg')
    im = Image.new('RGB', (100, 100))
    im.save(temp_image)

    return temp_image


def authorize_user(case: APITestCase, user: User):
    token = AuthToken.objects.create(user, 'dummy')
    case.client.credentials(HTTP_AUTHORIZATION=f'Token {token.token}')


class CreateOfferTests(APITestCase):
    def setUp(self) -> None:
        self.url = reverse('offer-list')
        self.user = create_dummy_user(1)
        self.data = get_test_offer_data(1)

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
        self.data = get_test_offer_data(1)
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
        self.data = get_test_offer_data(1)
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
        self.data = get_test_offer_data(1)
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
        self.data = get_test_offer_data(1)
        self.data2 = get_test_offer_data(2)
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


class CreateOfferImageTests(APITestCase):
    def setUp(self) -> None:
        self.user = create_dummy_user(1)
        self.offer_data = get_test_offer_data(1)
        self.offer = Offer.objects.create(lender=self.user, **self.offer_data)
        self.url = reverse('offerimage-list')

        self.data = {
            'offer': self.offer.id,
        }

    def test_not_authenticated_cannot_create(self):
        r = self.client.post(self.url, data=self.data)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(OfferImage.objects.all().count(), 0)

    def test_not_offer_owner_cannot_create(self):
        not_owner = create_dummy_user(2)
        authorize_user(self, not_owner)

        tmp_image = get_temp_image_file()
        with open(tmp_image.name, 'rb') as f:
            self.data['image'] = f
            r = self.client.post(self.url, data=self.data)

        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(OfferImage.objects.all().count(), 0)

    def test_lender_can_create(self):
        authorize_user(self, self.user)

        tmp_image = get_temp_image_file()
        with open(tmp_image.name, 'rb') as f:
            self.data['image'] = f
            r = self.client.post(self.url, data=self.data)

        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OfferImage.objects.all().count(), 1)


class DeleteOfferImageTests(APITestCase):
    def setUp(self) -> None:
        self.user = create_dummy_user(1)
        self.offer_data = get_test_offer_data(1)
        self.offer = Offer.objects.create(lender=self.user, **self.offer_data)

        self.data = {
            'offer': self.offer,
            'image': 'tmp'
        }
        self.offer_image = OfferImage.objects.create(**self.data)
        self.url = reverse('offerimage-detail', args=(self.offer_image.id,))

    def test_not_authenticated_cannot_delete(self):
        r = self.client.delete(self.url)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(OfferImage.objects.all().count(), 1)

    def test_not_lender_cannot_delete(self):
        not_lender = create_dummy_user(2)
        authorize_user(self, not_lender)

        r = self.client.delete(self.url)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(OfferImage.objects.all().count(), 1)

    def test_lender_can_delete(self):
        authorize_user(self, self.user)

        r = self.client.delete(self.url)
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(OfferImage.objects.all().count(), 0)


class ReadOfferImageTests(APITestCase):
    def setUp(self) -> None:
        self.user = create_dummy_user(1)
        self.data = get_test_offer_data(1)
        self.data2 = get_test_offer_data(2)
        self.offer = Offer.objects.create(lender=self.user, **self.data)
        self.offer2 = Offer.objects.create(lender=self.user, **self.data2)

        self.image_data = {
            'offer': self.offer,
            'image': 'tmp1'
        }
        self.image_data2 = {
            'offer': self.offer2,
            'image': 'tmp2'
        }

        self.offer_image = OfferImage.objects.create(**self.image_data)
        self.offer_image2 = OfferImage.objects.create(**self.image_data2)
        self.url = reverse('offerimage-detail', args=(self.offer_image.id,))
        self.list_url = reverse('offerimage-list')

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
        offer_image = r.json()
        # Get filename of returned in response
        offer_image_file = offer_image['image'].split('/')[-1]

        self.assertEqual(offer_image_file, self.image_data['image'])
        self.assertEqual(offer_image['offer'], self.image_data['offer'].id)

        # list of objects
        r = self.client.get(self.list_url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        offer_images = r.json()
        self.assertEqual(len(offer_images), 2)

        offer_image = offer_images[0]
        # Get filename of returned in response
        offer_image_file = offer_image['image'].split('/')[-1]

        self.assertEqual(offer_image_file, self.image_data['image'])
        self.assertEqual(offer_image['offer'], self.image_data['offer'].id)

        offer_image2 = offer_images[1]
        # Get filename of returned in response
        offer_image_file = offer_image2['image'].split('/')[-1]

        self.assertEqual(offer_image_file, self.image_data2['image'])
        self.assertEqual(offer_image2['offer'], self.image_data2['offer'].id)
