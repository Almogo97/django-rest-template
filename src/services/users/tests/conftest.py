import pytest
from freezegun import freeze_time

from services.users import business_logic
from services.users.managers import UserManager
from services.users.models import RecoverPasswordCode


@pytest.fixture
def mock_create_user(mocker, user):
    return mocker.patch.object(UserManager, 'create_user', return_value=user)


@pytest.fixture
def mock_get_recover_password_code(mocker):
    return mocker.patch.object(
        business_logic,
        'get_recover_password_code',
        return_value='mocked',
    )


@pytest.fixture
def mock_send_email_with_recover_password_code(mocker):
    return mocker.patch.object(
        business_logic,
        'send_email_with_recover_password_code',
    )


@pytest.fixture
@freeze_time('2000-01-01 12:00:00')
def recover_password_code(user):
    return RecoverPasswordCode.objects.create(user=user)


@pytest.fixture
def mock_is_password_recover_code_valid(mocker):
    return mocker.patch.object(
        business_logic,
        'is_password_recover_code_valid',
    )


@pytest.fixture
def mock_change_password_with_code(mocker):
    return mocker.patch.object(
        business_logic,
        'change_password_with_code',
    )
