import pytest
from django.conf import settings

from services.users.business_logic import (
    get_recover_password_code,
    send_email_with_recover_password_code
)
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


@pytest.mark.django_db
class TestSendEmailWithRecoverPasswordCode:
    def test_sends_email_if_user_exists(
            self, user, mock_send_templated_email, mock_get_recover_password_code):
        email = user.email
        send_email_with_recover_password_code(email)

        mock_get_recover_password_code.assert_called_once_with(user)
        mock_send_templated_email.assert_called_once_with(
            [email], 'recover_password_code', context={'code': 'mocked'}
        )

    def test_does_not_send_email_if_user_does_not_exists(
            self, mock_send_templated_email, mock_get_recover_password_code):
        send_email_with_recover_password_code('test@test.es')

        mock_get_recover_password_code.assert_not_called()
        mock_send_templated_email.assert_not_called()
