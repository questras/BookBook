from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from token_auth.auth import TokenAuthentication
from .serializers import UserMessageSerializer, CreateUserMessageSerializer


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
