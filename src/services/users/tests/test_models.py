import pytest
from django.conf import settings

from services.users.models import RecoverPasswordCode


@pytest.mark.django_db
class TestRecoverPasswordCode:
    def test_id_is_a_random_string_of_certain_length(self, user):
        code = RecoverPasswordCode.objects.create(user=user)

        assert len(code.id) == settings.RECOVER_PASSWORD_CODE_LENGTH
