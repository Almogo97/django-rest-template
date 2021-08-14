from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AccountRecoveryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'services.account_recovery'
    verbose_name = _('account recovery')
