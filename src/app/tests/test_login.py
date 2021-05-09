import pytest


@pytest.mark.django_db
@pytest.mark.usefixtures('user')
class TestLoginView:
    uri = '/auth/token/'

    def test_returns_200(self, client, api):
        response = client.post(
            self.uri,
            {
                'client_id': api.client_id,
                'client_secret': api.client_secret,
                'grant_type': 'password',
                'username': 'test@test.es',
                'password': '12345678A',
            }
        )

        assert response.status_code == 200

    def test_returns_200_with_json_content(self, client, api):
        response = client.post(
            self.uri,
            {
                'client_id': api.client_id,
                'client_secret': api.client_secret,
                'grant_type': 'password',
                'username': 'test@test.es',
                'password': '12345678A',
            },
            content_type='application/json'
        )

        assert response.status_code == 200

    def test_returns_400_when_credentials_are_invalid(self, client, api):
        response = client.post(
            self.uri,
            {
                'client_id': api.client_id,
                'client_secret': api.client_secret,
                'grant_type': 'password',
                'username': 'test@test.es',
                'password': 'incorrect',
            }
        )

        assert response.status_code == 400
