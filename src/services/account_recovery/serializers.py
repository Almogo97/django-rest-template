from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from services.account_recovery import business_logic
from services.users.serializers import PasswordField


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordRecoverCodeSerializer(serializers.Serializer):
    code = serializers.CharField()

    def validate_code(self, code):
        if not business_logic.is_password_recover_code_valid(code):
            raise serializers.ValidationError(_('Code is not valid'))
        return code


class ChangePasswordWithCodeSerializer(PasswordRecoverCodeSerializer):
    password = PasswordField(write_only=False)
