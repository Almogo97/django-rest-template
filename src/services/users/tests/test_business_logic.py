import pytest
from django.conf import settings

from services.users.business_logic import get_recover_password_code
from services.users.models import RecoverPasswordCode


@pytest.mark.django_db
class TestGetRecoverPasswordCode():
    def test_creates_code_if_it_does_not_exist(self, user):
        assert RecoverPasswordCode.objects.count() == 0
        get_recover_password_code(user)
        assert RecoverPasswordCode.objects.count() == 1

    def test_returns_code_as_str(self, user):
        code = get_recover_password_code(user)
        assert isinstance(code, str)
        assert len(code) == settings.RECOVER_PASSWORD_CODE_LENGTH

    def test_returns_existing_code(self, user):
        code = RecoverPasswordCode.objects.create(user=user)
        assert code.id == get_recover_password_code(user)
