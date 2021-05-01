import re

from rest_framework import serializers

from .models import Offer, OfferImage
from users.serializers import CustomUserSerializer

polish_phone_number_regex = r'(\+48){0,1}\s*([0-9]\s*){9}'


class OfferImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferImage
        fields = ('id', 'image', 'offer')


class OfferSerializer(serializers.ModelSerializer):
    lender = CustomUserSerializer(
        read_only=True  # don't allow to specify lender in request,
                        # it will be done based on authentication.
    )
    created = serializers.DateTimeField(
        format='%Y-%m-%d %H:%M:%S',
        read_only=True
    )
    updated = serializers.DateTimeField(
        format='%Y-%m-%d %H:%M:%S',
        read_only=True
    )
    images = OfferImageSerializer(
        source='offerimage_set',
        read_only=True,
        many=True
    )

    class Meta:
        model = Offer
        fields = ('id', 'title', 'author', 'description',
                  'state', 'city', 'status', 'created', 'updated',
                  'lender', 'lender_phone', 'images')
        read_only_fields = ('id', 'status')

    def validate_lender_phone(self, value):
        """Check whether phone number is correct, polish
        phone number."""

        if not re.fullmatch(polish_phone_number_regex, value):
            raise serializers.ValidationError('Incorrect phone number')

        # Remove unnecessary spacing
        value = value.replace(' ', '')
        return value
