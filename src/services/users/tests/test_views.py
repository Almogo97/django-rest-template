import pytest


@pytest.mark.django_db
@pytest.mark.usefixtures('mock_send_templated_email')
class TestCreateUser:
    uri = '/users/'
    email = 'test2@test.es'
    password = 'qsd23fg098c'

    def test_returns_201(self, client, mock_create_user):
        response = client.post(self.uri, {'email': self.email, 'password': self.password})

        assert response.status_code == 201
        mock_create_user.assert_called_once_with(email=self.email, password=self.password)

    def test_returns_400_when_email_not_valid(self, client, mock_create_user):
        response = client.post(self.uri, {'email': 'test', 'password': self.password})

        assert response.status_code == 400
        assert 'email' in response.json()
        mock_create_user.assert_not_called()

    def test_returns_400_when_password_less_than_8_characters(
            self, client, mock_create_user):
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

    def test_returns_401_when_user_not_logged(self, client):
        response = client.get(self.uri)

        assert response.status_code == 401

    def test_returns_200(self, client_user):
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

    def test_returns_401_when_user_not_logged(self, client):
        response = client.delete(self.uri)

        assert response.status_code == 401

    def test_returns_204(self, client_user):
        response = client_user.delete(self.uri)

        assert response.status_code == 204
        assert response.content == b''


@pytest.mark.django_db
class TestUpdateMe:
    uri = '/users/me/'

    def test_returns_401_when_user_not_logged(self, client):
        response = client.patch(self.uri)

        assert response.status_code == 401

    def test_returns_200(self, client_user, user):
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
            'firebase_id': None,
        }
        assert user.email == 'test@test.es'
        assert user.first_name == 'Test'
        assert user.password.startswith('pbkdf2_sha256')
        assert user.password != old_password


@pytest.mark.django_db
class TestSendRecoverCodeEmail:
    uri = '/users/recover_password/'

    def test_returns_204(self, client, mock_send_email_with_recover_password_code):
        email = 'test@test.es'
        response = client.post(self.uri, {'email': email})

        assert response.status_code == 204
        mock_send_email_with_recover_password_code.assert_called_once_with(email)

    def test_returns_400_when_email_format_is_not_valid(self, client):
        response = client.post(self.uri, {'email': 'test'})

        assert response.status_code == 400
        assert 'email' in response.json()


@pytest.mark.django_db
class TestIsRecoverPasswordCodeValid:
    uri = '/users/is_recover_password_code_valid/'

    def test_returns_200_and_is_valid(self, client, mock_is_password_recover_code_valid):
        mock_is_password_recover_code_valid.return_value = True
        response = client.post(self.uri, {'code': '1234'})

        mock_is_password_recover_code_valid.assert_called_once_with('1234')
        assert response.status_code == 200
        assert response.json()['is_valid'] is True

    def test_returns_200_and_is_invalid(
            self, client, mock_is_password_recover_code_valid):
        mock_is_password_recover_code_valid.return_value = False
        response = client.post(self.uri, {'code': '1234'})

        mock_is_password_recover_code_valid.assert_called_once_with('1234')
        assert response.status_code == 200
        assert response.json()['is_valid'] is False


@pytest.mark.django_db
class TestChangePassword:
    uri = '/users/change_password/'

    def test_returns_204(
            self, client, mock_change_password_with_code,
            mock_is_password_recover_code_valid):
        mock_is_password_recover_code_valid.return_value = True
        response = client.post(self.uri, {'code': '1234', 'password': 'new_password'})

        mock_change_password_with_code.assert_called_once_with(
            code='1234',
            password='new_password',
        )
        assert response.status_code == 204
