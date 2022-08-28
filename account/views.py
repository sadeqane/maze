from django.db.models import ProtectedError
from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from account.models import User
from account.serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        if self.request.method in ["PUT", "PATCH"]:
            return UserUpdateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return []
        else:
            return [permission() for permission in self.permission_classes]

    def destroy(self, request, *args, **kwargs):
        try:
            super().destroy(request, *args, **kwargs)
        except ProtectedError as e:
            raise ValidationError(_("The user has many products in the store, so delete the products first"))
