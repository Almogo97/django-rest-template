import pytest


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
