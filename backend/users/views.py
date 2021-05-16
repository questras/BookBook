from rest_framework.generics import (
    UpdateAPIView,
    RetrieveAPIView,
    CreateAPIView
)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model


from token_auth.auth import TokenAuthentication
from .serializers import (
    ChangePasswordSerializer,
    CustomUserSerializer,
    RegistationSerializer
)


User = get_user_model()


class ChangePasswordView(UpdateAPIView):
    """View to change user's password."""

    model = User
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    http_method_names = ['put']

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.data.get('old_password')):
                return Response(
                    {'old_password': ['Wrong password.']},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.set_password(serializer.data.get('new_password'))
            user.save()

            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(RetrieveAPIView):
    """View to get user's profile data specified in serializer."""

    queryset = User.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer
    model = User


class MyProfileView(APIView):
    """View to get current user's profile data."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegistrationView(CreateAPIView):
    """Basic user registration without any kind of email validation"""
    serializer_class = RegistationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(None, status=status.HTTP_201_CREATED)
