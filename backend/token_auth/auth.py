from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions

from .models import AuthToken

AUTH_HEADER_PREFIX = b'token'


class TokenAuthentication(BaseAuthentication):
    """
    Authentication scheme for REST API, specifcally :class: `token_auth.models.AuthToken`.
    Matches HTTP AUTH header value to tokens stored in database and returns matching user.
    Sets ``request.user`` and ``request.auth``.
    """

    model = AuthToken

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != AUTH_HEADER_PREFIX:
            return None

        if len(auth) != 2:
            raise exceptions.AuthenticationFailed('Invalid auth header')

        return self.authenticate_token(auth[1])

    def authenticate_token(self, token):
        """ Verifies given token and returns objects"""
        token = token.decode("utf-8")

        try:
            auth_token = AuthToken.objects.get(token=token)

            if auth_token.is_expired:
                auth_token.delete()
                raise exceptions.AuthenticationFailed("token has expired")

            if not auth_token.user.is_active:
                raise exceptions.AuthenticationFailed("user is not active")

            return (auth_token.user, auth_token)
        except exceptions.AuthenticationFailed as e:
            raise exceptions.AuthenticationFailed(e)
        except Exception:
            # raise exception if AuthToken was not found
            raise exceptions.AuthenticationFailed("invalid token")
