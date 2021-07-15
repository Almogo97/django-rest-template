import pytest


@pytest.mark.django_db
@pytest.mark.usefixtures('user')
class TestLoginView:
    uri = '/auth/token/'

    def generate_request_body(self, api, username='test@test.es', password='12345678A'):
        return {
            'client_id': api.client_id,
            'client_secret': api.client_secret,
            'grant_type': 'password',
            'username': username,
            'password': password,
        }

    def test_returns_200_with_form_data(self, client, api):
        response = client.post(
            self.uri,
            self.generate_request_body(api)
        )

        assert response.status_code == 200

    def test_returns_200_with_json_content(self, client, api):
        response = client.post(
            self.uri,
            self.generate_request_body(api),
            content_type='application/json'
        )

        assert response.status_code == 200

    def test_returns_400_when_credentials_are_invalid(self, client, api):
        response = client.post(
            self.uri,
            self.generate_request_body(api, password='incorrect'),
        )

        assert response.status_code == 400

    def test_returns_400_when_user_is_inactive(self, user, client, api):
        user.is_active = False
        user.save()
        response = client.post(
            self.uri,
            self.generate_request_body(api)
        )

        assert response.status_code == 400
