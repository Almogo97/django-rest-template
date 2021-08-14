import pytest
from django.conf import settings
from django.db.utils import IntegrityError

from services.account_recovery.models import RecoverPasswordCode


@pytest.mark.django_db
class TestRecoverPasswordCode:
    def test_id_is_a_random_string_of_certain_length(self, recover_password_code):
        assert isinstance(recover_password_code.id, str)
        assert len(recover_password_code.id) == settings.RECOVER_PASSWORD_CODE_LENGTH

    def test_limit_one_code_per_user(self, recover_password_code):
        with pytest.raises(IntegrityError) as execinfo:
            RecoverPasswordCode.objects.create(user=recover_password_code.user)
        assert 'duplicate key value violates unique constraint' in str(execinfo.value)
