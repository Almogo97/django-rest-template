import pytest

from services.users.managers import UserManager
from services.users.models import RecoverPasswordCode


@pytest.fixture
def mock_create_user(mocker, user):
    return mocker.patch.object(UserManager, 'create_user', return_value=user)


@pytest.fixture
def recover_password_code(user):
    return RecoverPasswordCode.objects.create(user=user)
