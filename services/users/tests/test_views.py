from services.users.managers import UserManager
import pytest


@pytest.mark.django_db
class TestCreateUser:
    uri = '/users/'
    email = 'test2@test.es'
    password = '12345678'

    def test_returns_201(self, client, mock_create_user):
        response = client.post(self.uri, {'email': self.email, 'password': self.password})

        assert response.status_code == 201
        mock_create_user.assert_called_once_with(email=self.email, password=self.password)

    def test_returns_400_when_email_not_valid(self, client, mock_create_user):
        response = client.post(self.uri, {'email': 'test', 'password': self.password})

        assert response.status_code == 400
        assert 'email' in response.json()
        mock_create_user.assert_not_called()

    def test_returns_400_when_password_less_than_8_characters(self, client):
        response = client.post(self.uri, {'email': 'test@test.es', 'password': '1234'})

        assert response.status_code == 400
        assert 'password' in response.json() 
