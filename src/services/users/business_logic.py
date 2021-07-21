from services.users.models import RecoverPasswordCode


def get_recover_password_code(user):
    code, _ = RecoverPasswordCode.objects.get_or_create(user=user)
    return code.id
