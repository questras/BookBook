from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from datetime import timedelta
from secrets import token_urlsafe

User = get_user_model()

# Token expiration time
AUTH_TOKEN_TTL = timedelta(days=60)

# Number of entropy bytes in authorization token
AUTH_TOKEN_BYTES = 40


def _random_token():
    return token_urlsafe(AUTH_TOKEN_BYTES)


class AuthTokenManager(models.Manager):
    """ Custom AuthToken manager for automatic generation of token value """
    def create(self, user, device):
        token = _random_token()
        expires = timezone.now() + AUTH_TOKEN_TTL

        return super(AuthTokenManager, self).create(
            token=token,
            user=user,
            device=device,
            expires=expires
        )


class AuthToken(models.Model):
    """
    Simple expiring authorization token for REST API.
    One user can have many token for different devices.
    Each token can be anytime revoked and renewed.
    After expiring token is useless and will be renewed.
    """
    objects = AuthTokenManager()

    token = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        db_index=True,
        primary_key=True,
        help_text='Unique token string for authorization'
    )
    user = models.ForeignKey(
        User,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        help_text='User owning token'
    )
    created = models.DateTimeField(auto_now_add=True, help_text='Creation datetime of token')
    expires = models.DateTimeField(null=False, help_text='Expiration datetime of token. Can be extended with renew')
    device = models.CharField(max_length=200, blank=False, help_text="User device using given token")

    @property
    def is_expired(self):
        """Checks if token has already expired"""
        return timezone.now() > self.expires

    def renew(self):
        """ Renews token so it will expire in ```AUTH_TOKEN_TTL``` from now"""
        expires = timezone.now() + AUTH_TOKEN_TTL
        self.expires = expires
        self.save(update_fields=['expires'])
        return expires

    def __str__(self):
        return "{} {} from {}".format(self.token, self.user, self.device)
