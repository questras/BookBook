from time import sleep

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import UserMessage
from token_auth.models import AuthToken

User = get_user_model()


def create_dummy_user(n: int):
    """Create user for testing purposes with
    `n` identifier"""

    return User.objects.create_user(email=f'test{n}@test.com', password='test_password')


def create_dummy_message(sender: User, receiver: User, n: int):
    """Create user message for testing purposes with `n` identifier
    and `sender` and `receiver` specified as in arguments."""

    return UserMessage.objects.create(
        title=f'test title {n}',
        body=f'test body {n}',
        sender=sender,
        receiver=receiver
    )


def authorize_user(case: APITestCase, user: User):
    token = AuthToken.objects.create(user, 'dummy')
    case.client.credentials(HTTP_AUTHORIZATION=f'Token {token.token}')


class TestSentMessagesView(APITestCase):
    def setUp(self) -> None:
        self.user1 = create_dummy_user(1)
        self.user2 = create_dummy_user(2)
        self.message1 = create_dummy_message(
            self.user1,
            self.user2,
            1
        )
        self.message2 = create_dummy_message(
            self.user2,
            self.user1,
            2
        )
        self.url = reverse('sent-messages')

    def test_unauthenticated_cannot_access(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_see_correct_sent_messages(self):
        authorize_user(self, self.user1)

        r = self.client.get(self.url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        data = r.json()
        self.assertEqual(len(data), 1)

        message = data[0]
        self.assertEqual(message['title'], self.message1.title)
        self.assertEqual(message['body'], self.message1.body)
        self.assertEqual(message['sender']['id'], self.message1.sender.id)
        self.assertEqual(message['receiver']['id'], self.message1.receiver.id)

    def test_result_is_in_descending_order(self):
        authorize_user(self, self.user1)

        later_message = create_dummy_message(self.user1, self.user2, 3)
        r = self.client.get(self.url)
        data = r.json()

        self.assertEqual(len(data), 2)
        first, second = data[0], data[1]
        self.assertEqual(first['title'], later_message.title)
        self.assertEqual(second['title'], self.message1.title)


class TestReceivedMessagesView(APITestCase):
    def setUp(self) -> None:
        self.user1 = create_dummy_user(1)
        self.user2 = create_dummy_user(2)
        self.message1 = create_dummy_message(
            self.user1,
            self.user2,
            1
        )
        self.message2 = create_dummy_message(
            self.user2,
            self.user1,
            2
        )
        self.url = reverse('received-messages')

    def test_unauthenticated_cannot_access(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_see_correct_sent_messages(self):
        authorize_user(self, self.user1)

        r = self.client.get(self.url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        data = r.json()
        self.assertEqual(len(data), 1)

        message = data[0]
        self.assertEqual(message['title'], self.message2.title)
        self.assertEqual(message['body'], self.message2.body)
        self.assertEqual(message['sender']['id'], self.message2.sender.id)
        self.assertEqual(message['receiver']['id'], self.message2.receiver.id)

    def test_result_is_in_descending_order(self):
        authorize_user(self, self.user1)

        later_message = create_dummy_message(self.user2, self.user1, 3)
        r = self.client.get(self.url)
        data = r.json()

        self.assertEqual(len(data), 2)
        first, second = data[0], data[1]
        self.assertEqual(first['title'], later_message.title)
        self.assertEqual(second['title'], self.message2.title)


class TestSendMessageView(APITestCase):
    def setUp(self) -> None:
        self.user1 = create_dummy_user(1)
        self.user2 = create_dummy_user(2)

        self.data = {
            'title': 'test title',
            'body': 'test body',
            'receiver': self.user2.id,
        }
        self.url = reverse('send-message')

    def test_unauthenticated_cannot_send_message(self):
        r = self.client.post(self.url, data=self.data)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(UserMessage.objects.all().count(), 0)

    def test_user_can_send_message(self):
        authorize_user(self, self.user1)

        r = self.client.post(self.url, data=self.data)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        self.assertEqual(UserMessage.objects.all().count(), 1)
        message = UserMessage.objects.all()[0]
        self.assertEqual(message.title, self.data['title'])
        self.assertEqual(message.body, self.data['body'])
        self.assertEqual(message.receiver, self.user2)
        self.assertEqual(message.sender, self.user1)
        self.assertEqual(message.read_at, None)

    def test_same_user_cannot_be_sender_and_receiver(self):
        authorize_user(self, self.user1)
        self.data['receiver'] = self.user1.id

        r = self.client.post(self.url, data=self.data)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(UserMessage.objects.all().count(), 0)

    def test_cannot_send_message_to_non_existing_user(self):
        authorize_user(self, self.user1)
        self.data['receiver'] = 42000

        r = self.client.post(self.url, data=self.data)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(UserMessage.objects.all().count(), 0)

    def test_cannot_send_message_with_incomplete_data(self):
        authorize_user(self, self.user1)

        for key in self.data:
            data_copy = self.data.copy()
            data_copy[key] = ''
            r = self.client.post(self.url, data=data_copy)
            self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(UserMessage.objects.all().count(), 0)


class TestReadMessageView(APITestCase):
    def setUp(self) -> None:
        self.user1 = create_dummy_user(1)
        self.user2 = create_dummy_user(2)
        self.message1 = create_dummy_message(
            self.user1,
            self.user2,
            1
        )
        self.url = reverse('read-message', args=(self.message1.id,))

    def test_unauthenticated_cannot_access(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_read_when_is_not_receiver_nor_sender(self):
        new_user = create_dummy_user(3)
        authorize_user(self, new_user)

        r = self.client.get(self.url)
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_receiver_can_read(self):
        authorize_user(self, self.user2)

        r = self.client.get(self.url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        message = r.json()
        self.assertEqual(message['title'], self.message1.title)
        self.assertEqual(message['body'], self.message1.body)

    def test_user_sender_can_read(self):
        authorize_user(self, self.user1)

        r = self.client.get(self.url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        message = r.json()
        self.assertEqual(message['title'], self.message1.title)
        self.assertEqual(message['body'], self.message1.body)

    def test_read_at_doesnt_change_when_sender_reads(self):
        authorize_user(self, self.user1)

        # read_at is a null before reading.
        message = UserMessage.objects.all()[0]
        self.assertEqual(message.read_at, None)

        r = self.client.get(self.url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        # read_at is still a null because sender read it, not receiver.
        message = UserMessage.objects.all()[0]
        self.assertEqual(message.read_at, None)

    def test_read_at_changes_when_receiver_reads(self):
        authorize_user(self, self.user2)

        # read_at is a null before reading.
        message = UserMessage.objects.all()[0]
        self.assertEqual(message.read_at, None)

        r = self.client.get(self.url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        # read_at is not null because receiver read it.
        message = UserMessage.objects.all()[0]
        self.assertNotEqual(message.read_at, None)

    def test_read_at_changes_only_once(self):
        authorize_user(self, self.user2)

        # read_at is a null before reading.
        message = UserMessage.objects.all()[0]
        self.assertEqual(message.read_at, None)

        r = self.client.get(self.url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        # read_at is not null because receiver read it.
        message = UserMessage.objects.all()[0]
        self.assertNotEqual(message.read_at, None)

        old_read_at = message.read_at
        sleep(1)

        # Read again and check whether read_at changed.
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        message = UserMessage.objects.all()[0]
        # read_at shouldn't change.
        self.assertEqual(message.read_at, old_read_at)
