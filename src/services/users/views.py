from oauth2_provider.contrib.rest_framework.permissions import TokenHasReadWriteScope
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from services.users.entities import User
from services.users.serializers import RetrieveUserSerializer, UserSerializer


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'me':
            return RetrieveUserSerializer
        return UserSerializer

    @action(detail=False, permission_classes=(IsAuthenticated, TokenHasReadWriteScope))
    def me(self, request: Request):
        """Returns information about the logged in user"""
        return Response(self.get_serializer(request.user).data)

    @me.mapping.delete
    def delete_me(self, request: Request):
        """Deletes the logged in user"""
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @me.mapping.patch
    @me.mapping.put
    def update_me(self, request: Request):
        """Updates information about the logged in user"""
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
