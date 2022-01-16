import pytest
from django.conf import settings
from freezegun import freeze_time

from services.account_recovery.business_logic import (
    change_password_with_code,
    get_recover_password_code,
    is_password_recover_code_valid,
    send_email_with_recover_password_code,
)
from services.account_recovery.models import RecoverPasswordCode


@pytest.mark.django_db
class TestGetRecoverPasswordCode:
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
        self, user, mock_send_templated_email, mock_get_recover_password_code
    ):
        email = user.email
        send_email_with_recover_password_code(email)

        mock_get_recover_password_code.assert_called_once_with(user)
        mock_send_templated_email.assert_called_once_with(
            [email], 'recover_password_code', context={'code': 'mocked'}
        )

    def test_does_not_send_email_if_user_does_not_exist(
        self, mock_send_templated_email, mock_get_recover_password_code
    ):
        send_email_with_recover_password_code('test@test.es')

        mock_get_recover_password_code.assert_not_called()
        mock_send_templated_email.assert_not_called()


@pytest.mark.django_db
class TestIsPasswordRecoverCodeValid:
    @freeze_time('2000-01-01 12:29:59')
    def test_returns_true_when_code_exists_and_not_expired(self, recover_password_code):
        assert is_password_recover_code_valid(recover_password_code) is True

    @pytest.mark.usefixtures('recover_password_code')
    def test_returns_false_when_code_does_not_exist(self):
        assert is_password_recover_code_valid('1234') is False

    @freeze_time('2000-01-01 12:30:01')
    def test_returns_false_when_code_has_expired(self, recover_password_code):
        assert is_password_recover_code_valid(recover_password_code) is False


@pytest.mark.django_db
class TestChangePasswordWithCode:
    def test_changes_password_and_deletes_code(self, user, recover_password_code):
        old_password = user.password
        change_password_with_code(recover_password_code, 'new_password')

        assert old_password != user.password
        assert user.password.startswith('pbkdf2_sha256')
        assert RecoverPasswordCode.objects.count() == 0
