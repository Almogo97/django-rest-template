from unittest.mock import Mock

import pytest

from services.users.managers import UserManager
from services.users.entities import User


@pytest.fixture
def mock_create_user(mocker: Mock, user: User):
    return mocker.patch.object(UserManager, 'create_user', return_value=user)
