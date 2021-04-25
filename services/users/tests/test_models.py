from services.users.models import User
import pytest
from django.core.exceptions import ValidationError


@pytest.mark.django_db
class TestCreateUser:
    def test_creates_user(self):
        user = User.objects.create_user(
            email='test2@test.es',
            password='test',
        )

        assert user.email == 'test2@test.es'
        assert user.password.startswith('pbkdf2_sha256')

    def test_creates_user_with_extra_fields(self):
        user = User.objects.create_user(
            email='test2@test.es',
            password='test',
            first_name='Test',
        )

        assert user.first_name == 'Test'

    def test_raises_error_when_invalid_email(self):
        with pytest.raises(ValidationError) as e:
            User.objects.create_user(
                email='test',
                password='test'
            )

        assert 'email' in e.value.message_dict
