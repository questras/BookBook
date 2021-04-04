from rest_framework import serializers, exceptions
from django.core import exceptions as django_exceptions
from django.contrib.auth import get_user_model, password_validation

from .models import AuthToken
User = get_user_model()


class CredentialsSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label='Email',
        write_only=True,
        required=True,
        allow_blank=False,
    )
    password = serializers.CharField(
        label='Password',
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True,
        allow_blank=False,
        required=True
    )
    device = serializers.CharField(
        label='Device', 
        required=True,
        allow_blank=False,
        write_only=True,
    )

    @staticmethod
    def authenticate(email, password):
        try:
            user = User.objects.get(email=email)

            if user.is_active and user.check_password(password):
                return user

        except Exception:
            # no User object
            return None

        return None

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        device = attrs.get('device')

        user = self.authenticate(email, password)

        if not user:
            raise serializers.ValidationError('Invalid credentials', code='authorization')

        attrs['user'] = user
        attrs['device'] = device
        return attrs


class RegistationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        label='Password',
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False}
        }

    def validate(self, data):
        user = User(**data)
        password = data.get('password')

        try:
            password_validation.validate_password(password=password, user=User)
        except django_exceptions.ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})

        return super(RegistationSerializer, self).validate(data)

    def create(self, validated_data):
        return User.objects.create_user(
            validated_data['email'],
            validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )


class AuthTokenSerializer(serializers.Serializer):
    token = serializers.CharField(
        label='Token',
        required=True,
        allow_blank=False
    )
