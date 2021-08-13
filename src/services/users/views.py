from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from services.users import business_logic
from services.users.models import User
from services.users.serializers import (
    EmailSerializer,
    PasswordRecoverCodeSerializer,
    RetrieveUserSerializer,
    UserSerializer
)


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'me':
            return RetrieveUserSerializer
        return UserSerializer

    @action(detail=False, permission_classes=(IsAuthenticated,))
    def me(self, request):
        return Response(self.get_serializer(request.user).data)

    @me.mapping.delete
    def delete_me(self, request):
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @me.mapping.patch
    @me.mapping.put
    def update_me(self, request):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserRecoverPasswordViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = EmailSerializer

    def get_serializer_class(self):
        if self.action == 'is_recover_password_code_valid':
            return PasswordRecoverCodeSerializer
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
        raise NotImplementedError
