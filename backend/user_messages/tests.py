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
