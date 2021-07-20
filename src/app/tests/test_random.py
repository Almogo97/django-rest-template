from django.conf import settings

from app.random import generate_password_recover_code


class TestGeneratePasswordRecoverCode:
    def test_generates_code_with_proper_length(self):
        code = generate_password_recover_code()

        assert len(code) == settings.RECOVER_PASSWORD_CODE_LENGTH
