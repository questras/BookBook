from rest_framework import serializers
from django.contrib.auth import get_user_model

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


class AuthTokenSerializer(serializers.Serializer):
    token = serializers.CharField(
        label='Token',
        required=True,
        allow_blank=False
    )
