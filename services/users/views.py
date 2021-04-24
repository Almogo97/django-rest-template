from services.users.serializers import BaseUserSerializer, CreateUserSerializer
from services.users.models import User
from rest_framework import mixins, viewsets


class UserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        return BaseUserSerializer
