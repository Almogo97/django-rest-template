from django.contrib.auth import password_validation
from rest_framework import serializers

from services.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'first_name', 'last_name', 'email', 'firebase_id')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password is not None:
            instance.set_password(password)

        return super().update(instance, validated_data)


class RetrieveUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ('first_name', 'last_name', 'email')


class PasswordField(serializers.CharField):

    def __init__(self, *args, **kwargs):
        kwargs['write_only'] = kwargs.pop('write_only', True)
        kwargs['style'] = {'input_type': 'password'}
        self.validate_password = kwargs.pop('validate_password', True)
        self.user = kwargs.pop('user', None)
        self.user_from_request = kwargs.pop('get_user_from_request', True)
        super(PasswordField, self).__init__(*args, **kwargs)

    def set_user(self, user):
        self.user = user

    def get_user(self):
        if not self.user and self.user_from_request:
            if self.context:
                request = self.context.get('request')
                if request.user.is_authenticated:
                    self.user = request.user
        return self.user

    def to_internal_value(self, data):
        if self.validate_password:
            password_validation.validate_password(data, user=self.get_user())
        return super(PasswordField, self).to_internal_value(data)
