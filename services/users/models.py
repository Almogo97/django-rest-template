from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    firebase_token = models.CharField(
        _('firebase token'),
        max_length=255,
        null=True,
        blank=True,
    )

    # Login with email
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        ordering = ('last_name', 'first_name')
        verbose_name = _('user')
        verbose_name_plural = _('users')
