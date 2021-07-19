import pytest
from rest_framework.test import APIClient

from services.users.models import User

"""
Helpers
"""


@pytest.fixture
def danq(django_assert_num_queries):
    return django_assert_num_queries


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
def client_user(user):
    token = user.oauth2_provider_accesstoken.create(token='token', expires='9999-01-01')
    client = APIClient()
    client.credentials(Authorization=f'Bearer {token}')
    return client


"""
Mail
"""


@pytest.fixture
def mock_send_templated_email(mocker):
    return mocker.patch('services.mail.send_templated_email')
