import pytest

from services import mail


@pytest.fixture
def mock_send_templated_email(mocker):
    return mocker.patch.object(mail, 'send_templated_email')
