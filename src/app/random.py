from django.conf import settings
from django.utils.crypto import get_random_string


def generate_password_recover_code():
    return get_random_string(settings.RECOVER_PASSWORD_CODE_LENGTH)
