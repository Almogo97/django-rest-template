from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class UserModel(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)

    # Login with email
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects: UserManager = UserManager()

    class Meta:
        ordering = ('last_name', 'first_name')
