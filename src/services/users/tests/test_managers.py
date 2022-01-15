from unittest.mock import Mock

import pytest
from django.core.exceptions import ValidationError

from services.users.entities import User


@pytest.mark.django_db
@pytest.mark.usefixtures('mock_send_templated_email')
class TestCreateUser:
    def test_creates_user(self):
        user = User.objects.create_user(
            email='test2@test.com',
            password='test',
        )

        assert user.email == 'test2@test.com'
        assert user.password.startswith('pbkdf2_sha256')

    def test_creates_user_with_extra_fields(self):
        user = User.objects.create_user(
            email='test2@test.com',
            password='test',
            first_name='Test',
        )

        assert user.first_name == 'Test'

    def test_raises_error_when_invalid_email(self):
        with pytest.raises(ValidationError) as e:
            User.objects.create_user(email='test', password='test')

        assert 'email' in e.value.message_dict

    def test_sends_welcome_mail(self, mock_send_templated_email: Mock):
        User.objects.create_user(email='test2@test.com', password='test')

        mock_send_templated_email.assert_called_once_with(['test2@test.com'], 'welcome')
