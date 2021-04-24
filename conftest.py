import pytest

from services.users.models import User


@pytest.fixture
def user():
    return User.objects.create(
        email='test@test.es',
    )


@pytest.fixture
def client_user(client, user):
    client.force_login(user)
    return client
