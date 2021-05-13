from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from token_auth.auth import TokenAuthentication
from .serializers import UserMessageSerializer


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
