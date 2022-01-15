import datetime

import pytest
from django.utils import timezone
from oauth2_provider.models import AccessToken
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
    user = User.objects.create_user(email='test@test.es', password='password')
    user.set_password('12345678A')
    user.save()
    return user


@pytest.fixture
def client_user(user: User):
    token: AccessToken = AccessToken.objects.create(
        user=user,
        token='1234567890',
        expires=timezone.now() + datetime.timedelta(days=1),
        scope='read write',
    )
    client = APIClient()
    client.credentials(Authorization=f'Bearer {token}')
    return client


"""
Mail
"""


@pytest.fixture
def mock_send_templated_email(mocker):
    return mocker.patch('services.mail.send_templated_email')
