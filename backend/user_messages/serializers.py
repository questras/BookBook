from rest_framework import serializers

from .models import UserMessage
from users.serializers import CustomUserSerializer


class UserMessageSerializer(serializers.ModelSerializer):
    sender = CustomUserSerializer(
        read_only=True  # Don't allow to specify sender in request,
                        # it will be done based on authentication.
    )
    receiver = CustomUserSerializer()

    class Meta:
        model = UserMessage
        fields = ('id', 'title', 'body', 'sender', 'receiver',
                  'created_at', 'read_at')
        read_only_fields = ('id', 'created_at', 'read_at', 'sender')
