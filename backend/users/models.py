from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """Custom user model with email as unique identifier."""
    email = models.EmailField(verbose_name='email address', unique=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # required fields to enter when creating superuser

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email
