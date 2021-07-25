from services import mail
from services.users.models import RecoverPasswordCode, User


def get_recover_password_code(user):
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
