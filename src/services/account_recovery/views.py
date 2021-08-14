from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from services.account_recovery import business_logic

from .serializers import (
    ChangePasswordWithCodeSerializer,
    EmailSerializer,
    PasswordRecoverCodeSerializer
)

User = get_user_model()


class UserRecoverPasswordViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'is_recover_password_code_valid':
            return PasswordRecoverCodeSerializer
        if self.action == 'change_password':
            return ChangePasswordWithCodeSerializer
        if self.action == 'recover_password':
            return EmailSerializer

    @action(detail=False, methods=['post'])
    def recover_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        business_logic.send_email_with_recover_password_code(
            serializer.validated_data.get('email'))
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'])
    def is_recover_password_code_valid(self, request):
        serializer = self.get_serializer(data=request.data)
        is_valid = serializer.is_valid()
        return Response({'is_valid': is_valid})

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        business_logic.change_password_with_code(
            code=serializer.data['code'],
            password=serializer.data['password'])
        return Response(status=status.HTTP_204_NO_CONTENT)
