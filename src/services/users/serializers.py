from typing import Any, Optional

from django.contrib.auth import password_validation
from django.contrib.auth.models import AbstractBaseUser
from rest_framework import serializers
from rest_framework.request import Request

from services.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'first_name', 'last_name', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value: str):
        password_validation.validate_password(value)
        return value

    def create(self, validated_data: dict[str, Any]) -> User:
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance: User, validated_data: dict[str, Any]) -> User:
        password = validated_data.pop('password', None)
        if password is not None:
            instance.set_password(password)

        return super().update(instance, validated_data)


class RetrieveUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ('first_name', 'last_name', 'email')


class PasswordField(serializers.CharField):
    def __init__(
        self,
        *args,
        validate_password: bool = True,
        user: Optional[AbstractBaseUser] = None,
        user_from_request: bool = True,
        **kwargs
    ):
        kwargs['write_only'] = kwargs.pop('write_only', True)
        kwargs['style'] = {'input_type': 'password'}
        self.validate_password = validate_password
        self.user = user
        self.user_from_request = user_from_request
        super(PasswordField, self).__init__(*args, **kwargs)

    def set_user(self, user: Optional[AbstractBaseUser]):
        self.user = user

    def get_user(self):
        if not self.user and self.user_from_request:
            if self.context:
                request: Request = self.context['request']
                user: AbstractBaseUser = request.user
                if user.is_authenticated:
                    self.user = user
        return self.user

    def to_internal_value(self, data: str):
        if self.validate_password:
            password_validation.validate_password(data, user=self.get_user())
        return super(PasswordField, self).to_internal_value(data)
