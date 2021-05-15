from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Q

from token_auth.auth import TokenAuthentication
from .serializers import UserMessageSerializer, CreateUserMessageSerializer
from .models import UserMessage


class ReceivedMessagesView(ListAPIView):
    """View to get messages that are sent to current user."""

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = UserMessageSerializer

    def get_queryset(self):
        return self.request.user.received_messages.all().order_by('-created_at')


class SentMessagesView(ListAPIView):
    """View to get messages that are sent by current user."""

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = UserMessageSerializer

    def get_queryset(self):
        return self.request.user.sent_messages.all().order_by('-created_at')


class SendMessageView(CreateAPIView):
    """View to send a message from one user to another."""

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = CreateUserMessageSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['current_user'] = self.request.user

        return context

    def perform_create(self, serializer):
        # Set sender to be currently authenticated user.
        serializer.validated_data['sender'] = self.request.user
        serializer.save()


class ReadMessageView(RetrieveAPIView):
    """View to read a single message. Once the message is
    read first time, its `read_at` field is changed
    to current datetime. Only users related to
    message(sender and receiver) can read it."""

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = UserMessageSerializer

    def get_queryset(self):
        return UserMessage.objects.filter(
            Q(receiver=self.request.user) |
            Q(sender=self.request.user)
        )

    def get_object(self):
        obj = super().get_object()
        if self.request.user == obj.receiver and obj.read_at is None:
            obj.read_at = timezone.now()
            obj.save()

        return obj
