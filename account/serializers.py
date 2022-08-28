from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import ReadOnlyField

from account.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['password']


class UserCreateSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    confirm_password = serializers.ReadOnlyField()
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        fields = [
            'username',
            'password',
            'confirm_password',
        ]
    def validate_username(self, value):
        if value in get_user_model().objects.values_list("username", flat=True):
            raise ValidationError({"username": _("username is duplicate")})
        return value

    def validate_password(self, value):
        data = self.initial_data.copy()
        confirm_password = data.pop('confirm_password')
        # user = get_user_model()(**data)
        if confirm_password != value:
            raise ValidationError(_("The confirm_password does not match"))
        try:
            validate_password(password=data['password'])
        except ValidationError as err:
            raise ValidationError({"password": str(err)})
        return value

    @transaction.atomic
    def create(self, validated_data):
        password = validated_data.pop('password')

        validated_data.pop('confirm_password', None)
        user = get_user_model()(**validated_data)
        user.set_password(password)
        user.save()
        return user



class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
        ]

    def validate_username(self, value):
        if value in get_user_model().objects.values_list("username", flat=True):
            raise ValidationError({"username": _("username is duplicate")})
        return value
