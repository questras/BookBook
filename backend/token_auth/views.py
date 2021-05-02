from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from .serializers import CredentialsSerializer, AuthTokenSerializer
from .auth import TokenAuthentication
from .models import AuthToken


class AcquireTokenView(GenericAPIView):
    """Authorizates user based on submitted email and password. Returns newly generated authorization token"""
    authentication_classes = []
    permission_classes = []
    serializer_class = CredentialsSerializer

    @staticmethod
    def format_response(user, auth_token):
        return {
            'expires': str(auth_token.expires),
            'token': auth_token.token
        }

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request.user = serializer.validated_data['user']
        device = serializer.validated_data['device']

        auth_token = AuthToken.objects.create(request.user, device)

        return Response(self.format_response(request.user, auth_token), status=status.HTTP_200_OK)


class RevokeTokenView(GenericAPIView):
    """Revokes given authorization token regardless of expiration"""
    serializer_class = AuthTokenSerializer

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            AuthToken.objects.get(token=serializer.validated_data['token']).delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response(None, status=status.HTTP_404_NOT_FOUND)


class RenewTokenView(APIView):
    """Extends lifetime of token used for authorization for this requst"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, format=None):
        expires = request.auth.renew()
        return Response({"expires": str(expires)}, status=status.HTTP_200_OK)
