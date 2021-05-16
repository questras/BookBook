import re
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth import get_user_model

from offers.models import Offer
from offers.serializers import polish_phone_number_regex
from users.serializers import CustomUserSerializer

from .models import Request

User = get_user_model()


class RequestSerializer(serializers.ModelSerializer):
    requester = CustomUserSerializer(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Request
        fields = ('id', 'offer', 'about', 'status', 'created', 'updated', 'requester', 'requester_phone')
        readonly = ('id', 'offer', 'status', 'created', 'updated')

        validators = [UniqueTogetherValidator(queryset=Request.objects.all(), fields=['requester', 'offer'])]

    def validate_requester_phone(self, value):
        """Check whether phone number is correct, polish
        phone number."""

        if not re.fullmatch(polish_phone_number_regex, value):
            raise serializers.ValidationError('Incorrect phone number')

        value = value.replace(' ', '')
        return value
