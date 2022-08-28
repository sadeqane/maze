from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import ReadOnlyField

from account.models import User
from maze.models import Maze


class WallsField(serializers.Field):
    """
    Custom field for walls field
    """

    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        return str(data)


class MazeSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
                                               default=serializers.CurrentUserDefault(),
                                               write_only=False)
    walls = WallsField()

    class Meta:
        model = Maze
        fields = '__all__'
        # read_only_fields = ['password', 'user_permissions']


class SolveMazeSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    path = serializers.ListField()
