from unittest.mock import Mock

import pytest
from django.test.client import Client

from services.users.models import User


@pytest.mark.django_db
@pytest.mark.usefixtures('mock_send_templated_email')
class TestCreateUser:
    uri = '/users/'
    email = 'test2@test.es'
    password = 'qsd23fg098c'

    def test_returns_201(self, client: Client, mock_create_user: Mock):
        response = client.post(
            self.uri, {'email': self.email, 'password': self.password}
        )

        assert response.status_code == 201
        mock_create_user.assert_called_once_with(
            email=self.email, password=self.password
        )

    def test_returns_400_when_email_not_valid(
        self, client: Client, mock_create_user: Mock
    ):
        response = client.post(self.uri, {'email': 'test', 'password': self.password})

        assert response.status_code == 400
        assert 'email' in response.json()
        mock_create_user.assert_not_called()

    def test_returns_400_when_password_less_than_8_characters(
        self, client: Client, mock_create_user: Mock
    ):
        response = client.post(
            self.uri,
            {'email': self.email, 'password': '1234'},
        )

        assert response.status_code == 400
        assert 'password' in response.json()
        mock_create_user.assert_not_called()


@pytest.mark.django_db
class TestRetrieveMe:
    uri = '/users/me/'

    def test_returns_401_when_user_not_logged(self, client: Client):
        response = client.get(self.uri)

        assert response.status_code == 401

    def test_returns_200(self, client_user: Client):
        response = client_user.get(self.uri)

        assert response.status_code == 200
        assert response.json() == {
            'email': 'test@test.es',
            'first_name': '',
            'last_name': '',
        }


@pytest.mark.django_db
class TestDeleteMe:
    uri = '/users/me/'

    def test_returns_401_when_user_not_logged(self, client: Client):
        response = client.delete(self.uri)

        assert response.status_code == 401

    def test_returns_204(self, client_user: Client):
        response = client_user.delete(self.uri)

        assert response.status_code == 204
        assert response.content == b''


@pytest.mark.django_db
class TestUpdateMe:
    uri = '/users/me/'

    def test_returns_401_when_user_not_logged(self, client: Client):
        response = client.patch(self.uri)

        assert response.status_code == 401

    def test_returns_200(self, client_user: Client, user: User):
        old_password = user.password
        response = client_user.patch(
            self.uri,
            {'first_name': 'Test', 'password': 'qsd23fg098c'},
        )
        user.refresh_from_db()

        assert response.status_code == 200
        assert response.json() == {
            'email': 'test@test.es',
            'first_name': 'Test',
            'last_name': '',
        }
        assert user.email == 'test@test.es'
        assert user.first_name == 'Test'
        assert user.password.startswith('pbkdf2_sha256')
        assert user.password != old_password
