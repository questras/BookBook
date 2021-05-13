from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import UserMessage
from users.serializers import CustomUserSerializer

User = get_user_model()


class UserMessageSerializer(serializers.ModelSerializer):
    sender = CustomUserSerializer()
    receiver = CustomUserSerializer()

    class Meta:
        model = UserMessage
        fields = ('id', 'title', 'body', 'sender', 'receiver',
                  'created_at', 'read_at')
        read_only_fields = fields


class CreateUserMessageSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(
        # Don't allow to specify sender in request,
        # it will be done based on authentication.
        required=False,
        read_only=True
    )
    receiver = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=True,
        write_only=False
    )

    class Meta:
        model = UserMessage
        fields = ('id', 'title', 'body', 'sender', 'receiver',
                  'created_at', 'read_at')
        read_only_fields = ('id', 'created_at', 'read_at', 'sender')

    def validate_receiver(self, value):
        """Check whether user who sends message and receiver are not
        the same user."""

        current_user = self.context['current_user']
        if current_user == value:
            raise serializers.ValidationError(
                'You cannot send message to yourself'
            )

        return value
