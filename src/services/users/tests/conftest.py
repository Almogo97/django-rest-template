import pytest

from services.users.managers import UserManager


@pytest.fixture
def mock_create_user(mocker, user):
    return mocker.patch.object(UserManager, 'create_user', return_value=user)


@pytest.fixture
def mock_send_templated_email(mocker):
    return mocker.patch('services.users.managers.send_templated_email')
