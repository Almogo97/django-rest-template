import pytest
from oauth2_provider.models import Application


@pytest.fixture
def api():
    return Application.objects.create(
        name='api',
        client_id='test_client_id',
        client_secret='test_client_secret',
        client_type='confidential',
        authorization_grant_type='password',
    )
