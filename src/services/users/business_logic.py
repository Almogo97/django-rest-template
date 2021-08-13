from datetime import timedelta
from typing import Union

from django.conf import settings
from django.utils import timezone

from services import mail
from services.users.models import RecoverPasswordCode, User


def get_recover_password_code(user) -> str:
    code, _ = RecoverPasswordCode.objects.get_or_create(user=user)
    return code.id


def send_email_with_recover_password_code(email):
    try:
        user = User.objects.get(email=email)
        code = get_recover_password_code(user)
        context = {'code': code}
        mail.send_templated_email([email], 'recover_password_code', context=context)
    except User.DoesNotExist:
        return


def is_password_recover_code_valid(code: Union[str, RecoverPasswordCode]) -> bool:
    code = code if isinstance(code, str) else code.id
    time_limit = timezone.now() - timedelta(
        seconds=settings.RECOVER_PASSWORD_CODE_DURATION_SECONDS)
    return RecoverPasswordCode.objects.filter(
        id=code,
        created_at__gte=time_limit,
    ).exists()


def change_password_with_code(code: Union[str, RecoverPasswordCode], new_password: str):
    code = code if isinstance(
        code, RecoverPasswordCode) else RecoverPasswordCode.objects.get(id=code)
    user = code.user
    user.set_password(new_password)
    user.save(update_fields=['password'])
    code.delete()
