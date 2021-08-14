
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from app.random import generate_password_recover_code


class RecoverPasswordCode(models.Model):
    id = models.CharField(
        max_length=settings.RECOVER_PASSWORD_CODE_LENGTH,
        primary_key=True,
        default=generate_password_recover_code,
        editable=False,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        verbose_name=_('user'),
        unique=True,
    )
    created_at = models.DateTimeField(
        verbose_name=_('creation date'),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _('recover password code')
        verbose_name_plural = _('recover password codes')
