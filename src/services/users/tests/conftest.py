import pytest

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
        return_value='mocked'
    )


@pytest.fixture
def recover_password_code(user):
    return RecoverPasswordCode.objects.create(user=user)
