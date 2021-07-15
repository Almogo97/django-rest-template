import pytest

from services.users.models import User

"""
Users
"""


@pytest.fixture
@pytest.mark.usefixtures('mock_send_templated_email')
def user():
    user = User.objects.create_user(
        email='test@test.es',
    )
    user.set_password('12345678A')
    user.save()
    return user


@pytest.fixture
def client_user(client, user):
    client.force_login(user)
    return client


"""
Mail
"""


@pytest.fixture
def mock_send_templated_email(mocker):
    return mocker.patch('services.mail.send_templated_email')
