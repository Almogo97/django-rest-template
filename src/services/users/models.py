
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from app.random import generate_password_recover_code

from .managers import UserManager


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    firebase_id = models.CharField(
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


class RecoverPasswordCode(models.Model):
    id = models.CharField(
        max_length=settings.RECOVER_PASSWORD_CODE_LENGTH,
        primary_key=True,
        default=generate_password_recover_code,
        editable=False,
    )
    user = models.ForeignKey(
        User,
        models.CASCADE,
        verbose_name=_('user')
    )
    created_at = models.DateTimeField(
        verbose_name=_('creation date'),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _('recover password code')
        verbose_name_plural = _('recover password codes')
